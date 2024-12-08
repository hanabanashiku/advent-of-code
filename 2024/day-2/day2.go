package main

import (
	"bufio"
	"math"
	"os"
	"strconv"
	"strings"
)

func parseReports() [][]int {
	// file, _ := os.Open("example.txt")
	file, _ := os.Open("input.txt")
	scanner := bufio.NewScanner(file)
	defer file.Close()

	var reports [][]int
	for scanner.Scan() {
		line := scanner.Text()
		var report []int

		for _, field := range strings.Fields(line) {
			value, _ := strconv.Atoi(field)
			report = append(report, value)
		}
		reports = append(reports, report)
	}

	return reports
}

func isSafe(report []int) bool {
	isIncreasing := report[len(report)-1] > report[0]

	for i := 1; i < len(report); i++ {
		x, y := report[i-1], report[i]
		difference := math.Abs(float64(y - x))

		switch {
		case isIncreasing && x > y,
			!isIncreasing && y > x,
			difference > 3,
			difference < 1:
			return false
		}
	}

	return true
}

func part1() {
	reports := parseReports()
	count := 0

	for i := 0; i < len(reports); i++ {
		if isSafe(reports[i]) {
			count++
		}
	}

	println("Part 1:")
	println(count)
}

func dampenReport(report []int) bool {
	for i := 0; i < len(report); i++ {
		subset := make([]int, len(report)-1)
		copy(subset, report[:i])
		copy(subset[i:], report[i+1:])

		if isSafe(subset) {
			return true
		}
	}

	return false
}

func part2() {
	reports := parseReports()
	count := 0

	for i := 0; i < len(reports); i++ {
		if isSafe(reports[i]) {
			count++
		} else if dampenReport(reports[i]) {
			count++
		}
	}

	println("Part 2:")
	println(count)
}

func main() {
	part1()
	part2()
}
