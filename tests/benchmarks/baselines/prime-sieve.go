package main

import (
	"fmt";
	"flag";
	"os";
	"time";
	"strconv";
	"runtime";
)


func sieve(left <-chan int, right chan<- int, prime int) {
	for {
		i := <- left
		if (i % prime) != 0 {
			right <- i
		}
	}
}

func generate(channel chan int) {
	i := 2
	for {
		channel <- i
		i++
	}
}

func prime_sieve(n int) int {
	channel := make(chan int)
	go generate(channel)
	sum := 0
	for i := 0; i < n; i++ {
		prime := <- channel
		sum = sum + prime
		ch1 := make(chan int)
		go sieve(channel, ch1, prime)
		channel = ch1
	}

	return sum
}

func main() {
	flag.Parse()
	threads, _ := strconv.Atoi(os.Getenv("CORES"));

	if threads < 1 {
		threads = 1
	}

	runtime.GOMAXPROCS(threads)

	upto := 100
	if flag.NArg() >= 1 {
		upto, _ = strconv.Atoi(flag.Arg(0))
	}

	tries := 100

	for i := 0; i < tries; i++ {
		t0 := time.Now()
		prime_sieve(upto)
		t1 := time.Now()
		fmt.Printf("go-primesieve-sync(%d): total: iterations=1 runtime: %dus\n", upto, (t1.Sub(t0) / 1000))
	}

}
