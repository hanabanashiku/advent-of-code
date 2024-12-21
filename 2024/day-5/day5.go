package main

import (
	"bufio"
	"os"
	"strconv"
	"strings"
)

func parseInput() ([][2]int, [][]int) {
	// file, _ := os.Open("example.txt")
	file, _ := os.Open("input.txt")
	scanner := bufio.NewScanner(file)

	var rules [][2]int
	var updates [][]int

	processingRules := true
	for scanner.Scan() {
		line := scanner.Text()

		if processingRules && !strings.Contains(line, "|") {
			processingRules = false
			continue
		}

		if processingRules {
			strs := strings.Split(line, "|")
			x, _ := strconv.Atoi(strs[0])
			y, _ := strconv.Atoi(strs[1])
			rules = append(rules, [2]int{x, y})
			continue
		}

		var update []int
		for _, str := range strings.Split(line, ",") {
			num, _ := strconv.Atoi(str)
			update = append(update, num)
		}
		updates = append(updates, update)

	}
	return rules, updates
}

func buildMaps(rules [][2]int) map[int][][2]int {
	lastMap := make(map[int][][2]int)

	for _, rule := range rules {
		if ruleGroup, ok := lastMap[rule[1]]; ok {
			lastMap[rule[1]] = append(ruleGroup, rule)
		} else {
			lastMap[rule[1]] = [][2]int{rule}
		}
	}

	return lastMap
}

func checkUpdate(lastMap map[int][][2]int, update []int) bool {
	foundMap := make(map[int]bool)
	allMap := make(map[int]bool)

	for _, page := range update {
		allMap[page] = true
	}

	for _, page := range update {
		for _, ruleByLast := range lastMap[page] {
			if allMap[ruleByLast[0]] && !foundMap[ruleByLast[0]] {
				return false
			}
		}

		foundMap[page] = true
	}

	return true
}

func swap(arr []int, i, j int) []int {
	t := arr[i]
	arr[i] = arr[j]
	arr[j] = t
	return arr
}

func insert(arr []int, value, i int) []int {
	if arr[i] == 0 {
		arr[i] = value
		return arr
	}

	newArr := make([]int, len(arr))
	copy(newArr, arr[:i])
	newArr[i] = value
	copy(newArr[i+1:], arr[i:len(arr)-1])
	return newArr
}

func orderUpdate(rules [][2]int, update []int) []int {
	ordered := make([]int, len(update))

	for i, page := range update {
		invalidIndices := make([]bool, len(update))

		for _, rule := range rules {
			switch page {
			case rule[0]:
				found := false
				for j := 0; j < i; j++ {
					if ordered[j] == rule[1] {
						found = true
					} else if found {
						invalidIndices[j] = true
					}
				}
				break

			case rule[1]:
				found := false
				for j := i - 1; j >= 0; j-- {
					if ordered[j] == rule[0] {
						found = true
					}
					if found {
						invalidIndices[j] = true
					}
				}
				break
			}
		}

		for j, isInvalid := range invalidIndices {
			if !isInvalid {
				ordered = insert(ordered, page, j)
				break
			}
		}
	}

	return ordered
}

func part1() {
	rules, updates := parseInput()
	lastMap := buildMaps(rules)
	middles := 0

	for _, update := range updates {
		if !checkUpdate(lastMap, update) {
			continue
		}

		middles += update[len(update)/2]
	}

	println("Part 1:")
	println(middles)
}

func part2() {
	rules, updates := parseInput()
	lastMap := buildMaps(rules)
	middles := 0

	for _, update := range updates {
		if checkUpdate(lastMap, update) {
			continue
		}

		ordered := orderUpdate(rules, update)
		middles += ordered[len(update)/2]
	}

	println("Part 2:")
	println(middles)
}

func main() {
	part1()
	part2()
}
