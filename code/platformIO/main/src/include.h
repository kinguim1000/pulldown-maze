#include <Arduino.h>
#include <Wire.h> // I2C library, required for MLX90614
#include <SparkFunMLX90614.h> //Click here to get the library: http://librarymanager/All#Qwiic_IR_Thermometer by SparkFun
#include "LCD.h"
#include "scanner.h"

double sqrt(double a){                          // Raíz quadrada
    double n = a;
    for(int i = 0; i < 20; i++){                //Se precisar de mais precisão, é só aumentar o número, mas para o erro ser maior que o limite mínimo de precisão para double, o input precisa ser maior que o valor máximo de double... para valores proximos de 1000000000, o erro é menor que 10^-22, que eu julgo ser aceitável
        n = n - ((n*n-a)/(2*n));                //Método de newton, baby :)
    }
    return n;
}

namespace StandardDeviation{
    class SD{                                   //Classe de desvio padrão :3
        public:
        double operator~() const{                     //Para, quando quiser ler, poder só usar "~" ao invés de uma função
            return (double)StandardDeviation;
        }
        SD(int BufferSize = 100){               // Seta o tamanho do buffer quando inicializa um membro dessa classe. Se não for especificado, é setado como 100
            Buffer = new double[BufferSize];    //Funciona, confia
            Size = BufferSize;
        }
        ~SD(){
            delete[] Buffer;                    // Por causa da maneira em qeu precisa fazer para dar certo, precisa definir uma coisa pra, quando for deletar um membro da classe, também desalocar a memória usada pelo buffer.
        }
        void SDAdd(double input){               //Função para adicionar um medimento ao membro da classe
            Buffer[Counter] = input;            //adiciona coisa ao buffer ciclico 
            double TempSize = Size;             //Para deixar tudo bonitinho
            if(IsBufferFull == false){          //Garante que, se o buffer não estiver cheioi, não vai tentar calcular SD ou média com valores não inicializados
                if((Counter + 2)%Size == 0){
                    IsBufferFull = true;
                }
                TempSize = Counter+1;
            }
            double TempAvg = 0;                 //Calculador e atualizador de média
            for(int i = 0;i<TempSize;i++){
                TempAvg += Buffer[i];
            }
            Average = TempAvg/(TempSize);
            double TempSD = 0;                  //Calculador e atualizador de desvio padrão
            for(int i = 0; i < TempSize; i++){
                TempSD += (Buffer[i] - Average)*(Buffer[i] - Average);
            }
            StandardDeviation = sqrt(TempSD/(TempSize));
            Counter = (Counter+1)%Size;
        }
        double Avg() const{                           //Retorna a média de todos os valores atualmente dentro do buffer
            return Average;
        }

        private:
        double Average;                         //Os nomes de variaveis são aotoexplicativos
        double StandardDeviation = 0;
        int Size;
        int Counter = 0;                        //Menos esse, isso é só uma coisinha que aponta para a proxima posição que vai receber input
        double* Buffer;
        bool IsBufferFull = false;

    };
}

namespace KalmanFilter{
    class Kalman{                               //Filtro de kalman. 
        public:
            Kalman(double in1 = 1,double in2 = 0.00001,double in3 = 0.1): P(in1),Q(in2),R(in3){}
            void update(double z){                         
                P += Q;                         //Vou mentir não, eu basicamente peguei isso pronto, isso é vudu demais pra mim, mas parece funcionar
                double K = (P/(P+R));           //"Kalman Gain", o que quer que isso signifique
                x += K*(z - x);
                P *= (1 - K);
            }
            operator double() const{            //Pra não ter que chamar absolutamente nada se quiser ler o valor atual
                return x;
            }
        private:
            double x;                           //Estimativa
            double P;                           //Covariancia do estado inicial (?)
            double Q;                           //Covariancia de ruido do processo (???)
            double R;                           //Covariancia de ruido da medição (???????)
    };
}

namespace Sensores{
    using namespace StandardDeviation;
    using namespace KalmanFilter;
    
    class SensorDeTemperatura{
        public:
            SensorDeTemperatura(int Endereco){
                SDT.begin(Endereco);
                SDT.setUnit(TEMP_K);
                                //Inserir código de escanear para encontrar o sensor com o coiso I2C. Retornar Erro se não encontrado
            }
            void Atualizar(){   //Inserir código de leitura de sensores aqui
                if(!SDT.read()){return;}
                ValorAtual = SDT.object();
                DesvioPadrao.SDAdd(ValorAtual);
                if(ValorAtual > DesvioPadrao.Avg()+3*~DesvioPadrao){Filtro.update(ValorAtual);}
                
                
            }
            operator double(){
                Atualizar();
                return ValorAtual;
            }
            double operator~(){                     //Para, quando quiser ler, poder só usar "~" ao invés de uma função
                Atualizar();
                return Filtro;
            }
            double Desvio(){
                Atualizar();
                return ~DesvioPadrao;
            }



        private:
            SD DesvioPadrao;
            Kalman Filtro;
            double ValorAtual;
            IRTherm SDT;
    };

    class SensorUltrassonico{
        public:
            SensorUltrassonico(int Pino){
                Pin = Pino;
                                //Inserir código de escanear para encontrar o sensor com o coiso I2C. Retornar Erro se não encontrado
            }
            void Atualizar(){   //Inserir código de leitura de sensores aqui
                pinMode(Pin, OUTPUT);
                digitalWrite(Pin, LOW);
                delayMicroseconds(2);
                digitalWrite(Pin, HIGH);
                delayMicroseconds(5);
                digitalWrite(Pin, LOW);
                pinMode(Pin, INPUT);
                ValorAtual = microsecondsToCentimeters(pulseIn(Pin, HIGH));
                delay(100);
            }
            operator double(){
                Atualizar();
                return ValorAtual;
            }
            



        private:
            int Pin;
            double ValorAtual;
            long microsecondsToCentimeters(long microseconds) {
                return microseconds / 29 / 2;
            }
    };
}

double* RGBtoCBCR(int r,int g, int b){return new double[3]{1,2,3};}
