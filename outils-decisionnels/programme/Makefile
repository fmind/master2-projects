# Variables
CC=gcc
CFLAGS="-Wall"
LDFLAGS="-lm"

# Filenames
EXEC = solver
SOURCES = $(wildcard *.c)
OBJECTS = $(SOURCES:.c=.o)

# Main target
default: $(OBJECTS)
	$(CC) $(OBJECTS) $(LDFLAGS) -o $(EXEC)

# Generic rule
%.o: %.c
	$(CC) -c $(CFLAGS) $< -o $@

clean:
	rm $(EXEC) $(OBJECTS)
