import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useGameStore = defineStore('game', () => {
  const currentQuestion = ref(null)
  const questionNumber = ref(1)
  const score = ref(0)
  const helps = ref({
    fiftyFifty: true,
    timeFreeze: true,
    swapQuestion: true
  })
  
  function resetGame() {
    currentQuestion.value = null
    questionNumber.value = 1
    score.value = 0
    helps.value = {
      fiftyFifty: true,
      timeFreeze: true,
      swapQuestion: true
    }
  }
  
  function useHelp(helpType) {
    if (helps.value[helpType]) {
      helps.value[helpType] = false
      return true
    }
    return false
  }
  
  function nextQuestion() {
    questionNumber.value++
  }
  
  function addScore(points) {
    score.value += points
  }
  
  return {
    currentQuestion,
    questionNumber,
    score,
    helps,
    resetGame,
    useHelp,
    nextQuestion,
    addScore
  }
})
