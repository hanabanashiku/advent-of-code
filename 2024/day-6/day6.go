package main

import (
	"bufio"
	"os"
)

func parseMap() ([][]rune, [2]int, rune) {
	// file, _ := os.Open("example.txt")
	file, _ := os.Open("input.txt")
	defer file.Close()
	scanner := bufio.NewScanner(file)
	var theMap [][]rune
	var startingPosition [2]int
	var startingDirection rune

	i := -1
	for scanner.Scan() {
		line := scanner.Text()
		var row []rune
		i++

		for j, ch := range line {
			switch ch {
			case '^':
				startingPosition = [2]int{i, j}
				startingDirection = 'n'
				row = append(row, '.')
				break
			case '>':
				startingPosition = [2]int{i, j}
				startingDirection = 'e'
				row = append(row, '.')
				break
			case '<':
				startingPosition = [2]int{i, j}
				startingDirection = 'w'
				row = append(row, '.')
				break
			case 'v':
				startingPosition = [2]int{i, j}
				startingDirection = 's'
				row = append(row, '.')
				break

			default:
				row = append(row, ch)
			}
		}
		theMap = append(theMap, row)
	}

	return theMap, startingPosition, startingDirection
}

func moveNext(theMap [][]rune, position [2]int, direction rune) ([2]int, rune) {
	next := position
	switch direction {
	case 'n':
		next = [2]int{position[0] - 1, position[1]}
		break
	case 'e':
		next = [2]int{position[0], position[1] + 1}
		break
	case 's':
		next = [2]int{position[0] + 1, position[1]}
		break
	case 'w':
		next = [2]int{position[0], position[1] - 1}
		break
	}

	if !isOutsideOfMap(theMap, next) && theMap[next[0]][next[1]] == '#' {
		next = position
		switch direction {
		case 'n':
			direction = 'e'
			break
		case 'e':
			direction = 's'
			break
		case 's':
			direction = 'w'
			break
		case 'w':
			direction = 'n'
			break
		}
	}
	return next, direction
}

func isOutsideOfMap(theMap [][]rune, position [2]int) bool {
	return position[0] < 0 || position[0] >= len(theMap) || position[1] < 0 || position[1] >= len(theMap[0])
}

func part1() {
	theMap, position, direction := parseMap()
	visited := make(map[[2]int]bool)

	for !isOutsideOfMap(theMap, position) {
		visited[position] = true
		position, direction = moveNext(theMap, position, direction)
	}

	println("Part 1:")
	println(len(visited))
}

func part2() {
	theMap, startingPosition, startingDirection := parseMap()
	count := 0

	for i := 0; i < len(theMap); i++ {
		for j := 0; j < len(theMap[0]); j++ {
			if startingPosition[0] == i && startingPosition[1] == j {
				continue
			}
			if theMap[i][j] == '#' {
				continue
			}

			visited := make(map[[2]int]bool)
			overlap := 0
			position := startingPosition
			direction := startingDirection
			theMap[i][j] = '#'

			for !isOutsideOfMap(theMap, position) {
				position, direction = moveNext(theMap, position, direction)

				if visited[position] {
					if overlap > len(theMap) {
						count++
						break
					} else {
						overlap++
					}
				} else {
					overlap = 0
					visited[position] = true
				}
			}
			theMap[i][j] = '.'
		}
	}

	println("Part 2:")
	println(count)
}

func main() {
	part1()
	part2()
}
