#include <unistd.h>

#include "MMInterface.h"

void messageFunction(void* arg);

int main()
{
	pthread_t messageBusThread;

	int tret1 = pthread_create(&messageBusThread, NULL, messageFunction, NULL);

	pthread_join(thread1, NULL);
}

void messageFunction(void* arg)
{

}
