/*
 * Go benchmark
 * ------------
 *
 * Author: C.G. Ritson
 * License: GPL v2
 * Date: 14/11/2009
 * Origin: http://github.com/concurrency/kroc
 *
 */

package main

import (
	"fmt";
	"flag";
	"os";
	"runtime";
	"strconv";
	"time";
)

const ELEMENTS = 256

func element(this, next chan int) {
	for {
		token := <-this;
		if token > 0 {
			next <- token + 1
		} else {
			next <- token;
			return
		}
	}
}

func root(cycles, tokens int, this, next chan int) {
	next <- 1;
	token := <-this;


	for i := 0; i < tokens; i = i + 1 {
		next <- i + 1
	}
	for cycles > 0 {
		for i := 0; i < tokens; i = i + 1 {
			token = <-this;
			next <- token + 1
		}
		cycles = cycles - 1
	}
	sum := 0;
	for i := 0; i < tokens; i = i + 1 {
		sum = sum + <-this
	}


	next <- 0;
	<-this;
}

func ring(cycles, tokens int) {
	head := make(chan int);
	this := head;

	for i := 0; i < ELEMENTS - 1; i = i + 1 {
		next := make(chan int);
		go element(this, next);
		this = next
	}

	root(cycles, tokens, this, head)
}

func main() {
	flag.Parse();

	threads, _ := strconv.Atoi(os.Getenv("CORES"));
	if threads < 1 {
		threads = 1
	}
	runtime.GOMAXPROCS(threads);

	cycles := 0;
	if flag.NArg() >= 1 {
		cycles, _ = strconv.Atoi(flag.Arg(0))
	}
	tokens := 1;
	if flag.NArg() >= 2 {
		tokens, _ = strconv.Atoi(flag.Arg(1))
	}
	sum := int64(0)
	tries := 10

	for i := 0; i < tries; i++ {
		t0 := time.Now()
		ring(cycles, tokens)
		t1 := time.Now()
		sum = sum + int64(t1.Sub(t0))
	}

	fmt.Printf("go-tokenring(%d, %d): total: iterations=%d runtime:%dus\n",cycles, tokens, tries, sum / int64(time.Microsecond))
}
