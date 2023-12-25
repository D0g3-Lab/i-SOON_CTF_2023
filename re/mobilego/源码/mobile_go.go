package game

import "math/rand"

var seed int64

func init() {
	seed = 2023
}
func Checkflag(flagin string) string {
	randlist := rand.New(rand.NewSource(seed))
	flag := []byte(flagin)
	for i := 0; i < len(flag); i++ {
		l := randlist.Intn(len(flag))
		r := randlist.Intn(len(flag))
		flag[l], flag[r] = flag[r], flag[l]
	}
	return string(flag)
}
