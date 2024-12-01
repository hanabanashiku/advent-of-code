package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
)

const useExample = false

func fileName() string {
	if useExample {
		return "ex.txt"
	} else {
		return "input.txt"
	}
}

func parseLists() ([]int, []int) {
	file, err := os.Open(fileName())
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var list1, list2 []int

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.Fields(line)

		num1, _ := strconv.Atoi(parts[0])
		num2, _ := strconv.Atoi(parts[1])

		list1 = append(list1, num1)
		list2 = append(list2, num2)
	}

	return list1, list2
}

func calculateDistances(list1, list2 []int) int {
	distance := 0
	for i := range len(list1) {
		distance += int(math.Abs(float64(list1[i] - list2[i])))
	}

	return distance
}

func calculateSimilarity(list1, list2 []int) int {
	score := 0

	occurances := make(map[int]int)

	for _, number := range list2 {
		occurances[number] += 1
	}

	for _, number := range list1 {
		score += number * occurances[number]
	}

	return score
}

func part1() {
	list1, list2 := parseLists()
	sort.Ints(list1)
	sort.Ints(list2)
	fmt.Println("Part 1:")
	fmt.Println(calculateDistances(list1, list2))
}

func part2() {
	list1, list2 := parseLists()
	fmt.Println("Part 2:")
	fmt.Println(calculateSimilarity(list1, list2))
}

func main() {
	part1()
	fmt.Println()
	part2()
}
