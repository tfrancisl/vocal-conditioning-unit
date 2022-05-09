TARGET = pitch_detection.out
OBJS = pitch_detection.o main.o
SRC = main.c pitch_detection.c

CFLAGS = -Wall -Wextra -O2
LFLAGS = -lm
CC = gcc

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) -o $(TARGET) $(OBJS) $(LFLAGS)

$(OBJS): $(SRC)
	$(CC) $(CFLAGS) -c $(SRC)

clean:
	rm -f *.o $(TARGET)