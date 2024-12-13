package main

import (
	"bufio"
	"os"
)

func parsePuzzle() [][]rune {
	// file, _ := os.Open("example.txt")
	file, _ := os.Open("input.txt")
	defer file.Close()

	var lines [][]rune
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, []rune(scanner.Text()))
	}

	return lines
}

func checkSpace(puzzle [][]rune, i, j int, direction string) (bool, [][2]int) {
	wordSize := len("XMAS")
	var word []rune
	var match [][2]int

	for n := 0; n < wordSize; n++ {
		var i1, j1 int

		switch direction {
		case "n":
			i1 = i - n
			j1 = j
			break
		case "s":
			i1 = i + n
			j1 = j
			break
		case "e":
			i1 = i
			j1 = j + n
			break
		case "w":
			i1 = i
			j1 = j - n
			break
		case "nw":
			i1 = i - n
			j1 = j - n
			break
		case "ne":
			i1 = i - n
			j1 = j + n
			break
		case "sw":
			i1 = i + n
			j1 = j - n
			break
		case "se":
			i1 = i + n
			j1 = j + n
			break
		}

		if i1 < 0 || i1 >= len(puzzle) {
			return false, [][2]int{}
		}
		if j1 < 0 || j1 >= len(puzzle[0]) {
			return false, [][2]int{}
		}

		word = append(word, puzzle[i1][j1])
		match = append(match, [2]int{i1, j1})
	}
	str := string(word)
	return str == "XMAS" || str == "SAMX", match
}

func part1() {
	puzzle := parsePuzzle()
	directions := []string{"n", "s", "w", "e", "nw", "ne", "sw", "se"}
	var matches [][][2]int
	count := 0

	for i := 0; i < len(puzzle); i++ {
		for j := 0; j < len(puzzle[0]); j++ {
			for _, direction := range directions {
				isMatch, match := checkSpace(puzzle, i, j, direction)

				if isMatch {
					count++
					matches = append(matches, match)
				}
			}
		}
	}
	println("Part 1:")
	println(count / 2)
}

func part2() {
	puzzle := parsePuzzle()
	count := 0

	for i := 1; i < len(puzzle)-1; i++ {
		for j := 1; j < len(puzzle[0])-1; j++ {
			x := []rune{puzzle[i-1][j-1], puzzle[i][j], puzzle[i+1][j+1]}
			y := []rune{puzzle[i-1][j+1], puzzle[i][j], puzzle[i+1][j-1]}

			isX := true
			for _, str := range []string{string(x), string(y)} {
				isX = isX && (str == "MAS" || str == "SAM")
			}

			if isX {
				count++
			}
		}
	}

	println("Part 2:")
	println(count)
}

func main() {
	part1()
	part2()
}
