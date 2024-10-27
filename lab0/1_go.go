package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
)

type SquareRoots struct {
	coefA     float64
	coefB     float64
	coefC     float64
	numRoots  int
	rootsList []float64
}

func (s *SquareRoots) Init() {
	s.coefA = 0.0
	s.coefB = 0.0
	s.coefC = 0.0
	s.numRoots = 0
	s.rootsList = []float64{}
}

func (s *SquareRoots) getCoef(index int, prompt string) float64 {
	if len(os.Args) > index {
		coefStr := os.Args[index]
		coef, err := strconv.ParseFloat(coefStr, 64)
		if err == nil {
			return coef
		}
		fmt.Println("Некорректная переменная")
	} else {
		fmt.Println(prompt)
		var coefStr string
		fmt.Scanln(&coefStr)
		coef, err := strconv.ParseFloat(coefStr, 64)
		if err == nil {
			return coef
		}
		fmt.Println("Некорректная переменная")
	}
	return s.getCoef(index, prompt)
}

func (s *SquareRoots) getCoefs() {
	s.coefA = s.getCoef(1, "Введите коэффициент A:")
	s.coefB = s.getCoef(2, "Введите коэффициент B:")
	s.coefC = s.getCoef(3, "Введите коэффициент C:")
}

func (s *SquareRoots) calculateRoots() {
	a := s.coefA
	b := s.coefB
	c := s.coefC

	D := b*b - 4*a*c
	if D == 0.0 {
		root := -b / (2.0 * a)
		if root == 0.0 {
			s.numRoots = 1
			s.rootsList = append(s.rootsList, root)
		} else if root > 0.0 {
			s.numRoots = 2
			s.rootsList = append(s.rootsList, math.Sqrt(root), -math.Sqrt(root))
		}
	} else if D > 0.0 {
		sqD := math.Sqrt(D)
		root1 := (-b + sqD) / (2.0 * a)
		root2 := (-b - sqD) / (2.0 * a)
		if root1 == 0.0 {
			s.numRoots++
			s.rootsList = append(s.rootsList, root1)
		} else if root1 > 0.0 {
			s.numRoots += 2
			s.rootsList = append(s.rootsList, math.Sqrt(root1), -math.Sqrt(root1))
		}
		if root2 == 0.0 {
			s.numRoots++
			s.rootsList = append(s.rootsList, root2)
		} else if root2 > 0.0 {
			s.numRoots += 2
			s.rootsList = append(s.rootsList, math.Sqrt(root2), -math.Sqrt(root2))
		}
	}
}

func (s *SquareRoots) printRoots() {
	if s.numRoots != len(s.rootsList) {
		fmt.Printf("Ошибка. Уравнение содержит %d действительных корней, но было вычислено %d корней.\n", s.numRoots, len(s.rootsList))
	} else {
		switch s.numRoots {
		case 0:
			fmt.Println("Нет корней")
		case 1:
			fmt.Printf("Один корень: %f\n", s.rootsList[0])
		case 2:
			fmt.Printf("Два корня: %f и %f\n", s.rootsList[0], s.rootsList[1])
		case 3:
			fmt.Printf("Три корня: %f, %f и %f\n", s.rootsList[0], s.rootsList[1], s.rootsList[2])
		case 4:
			fmt.Printf("Четыре корня: %f, %f, %f и %f\n", s.rootsList[0], s.rootsList[1], s.rootsList[2], s.rootsList[3])
		}
	}
}

func main() {
	var r SquareRoots
	r.Init()
	r.getCoefs()
	r.calculateRoots()
	r.printRoots()
}
