#include <windows.h>
#include <stdio.h>

int realrand(int min, int max)
{
    HMODULE advapi32 = LoadLibrary("Advapi32.dll");
    if (!advapi32)
    {
        printf("Failed to load Advapi32.dll\n");
        return 1;
    }

    BOOLEAN (APIENTRY *RtlGenRandom)(PVOID, ULONG) = (BOOLEAN (APIENTRY *)(PVOID, ULONG))GetProcAddress(advapi32, "SystemFunction036");
    if (!RtlGenRandom)
    {
        printf("Failed to get address of RtlGenRandom\n");
        return 1;
    }

    unsigned char buffer[4];
    if (!RtlGenRandom(buffer, 4))
    {
        printf("RtlGenRandom failed\n");
        return 1;
    }

    unsigned int random_number = *(unsigned int *)buffer;

    int range = max - min + 1;
    int result = (random_number % range) + min;

    return result;
}
