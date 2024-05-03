PLOTOUT = ./plot

all: 
	mkdir ${PLOTOUT} -p
	gnuplot -e 'outdir="${PLOTOUT}"' plot/*.gnuplot

.PHONY: clean

clean:
	rm ./plot/*.png