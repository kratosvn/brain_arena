<template>
  <div class="home-view min-h-screen flex flex-col items-center justify-center p-8">
    <div class="text-center max-w-4xl">
      <!-- Logo/Title -->
      <h1 class="text-6xl font-bold text-white mb-4 animate-pulse">
        🧠 Đấu Trường Tri Thức
      </h1>
      <p class="text-2xl text-purple-300 mb-12 font-light">
        Brain Arena: Only the Smart Survive
      </p>
      
      <!-- Main Menu -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
        <button 
          @click="startGame"
          class="menu-button bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold py-6 px-8 rounded-xl text-xl transition-all transform hover:scale-105 shadow-2xl"
        >
          🎮 Chơi Ngay
        </button>
        
        <button 
          @click="goToLeaderboard"
          class="menu-button bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-bold py-6 px-8 rounded-xl text-xl transition-all transform hover:scale-105 shadow-2xl"
        >
          🏆 Bảng Xếp Hạng
        </button>
        
        <button 
          @click="goToShop"
          class="menu-button bg-gradient-to-r from-yellow-600 to-orange-600 hover:from-yellow-700 hover:to-orange-700 text-white font-bold py-6 px-8 rounded-xl text-xl transition-all transform hover:scale-105 shadow-2xl"
        >
          🛒 Cửa Hàng
        </button>
        
        <button 
          @click="goToProfile"
          class="menu-button bg-gradient-to-r from-green-600 to-teal-600 hover:from-green-700 hover:to-teal-700 text-white font-bold py-6 px-8 rounded-xl text-xl transition-all transform hover:scale-105 shadow-2xl"
        >
          👤 Hồ Sơ
        </button>
      </div>
      
      <!-- Features -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-white">
        <div class="feature-card bg-white/10 backdrop-blur-lg rounded-lg p-6">
          <div class="text-4xl mb-2">🤖</div>
          <h3 class="font-bold mb-2">AI Voice Narrator</h3>
          <p class="text-sm text-gray-300">10 giọng miễn phí + Premium voices</p>
        </div>
        
        <div class="feature-card bg-white/10 backdrop-blur-lg rounded-lg p-6">
          <div class="text-4xl mb-2">⚔️</div>
          <h3 class="font-bold mb-2">PvP Mode</h3>
          <p class="text-sm text-gray-300">Đối đầu 1v1 real-time</p>
        </div>
        
        <div class="feature-card bg-white/10 backdrop-blur-lg rounded-lg p-6">
          <div class="text-4xl mb-2">💡</div>
          <h3 class="font-bold mb-2">AI Hints</h3>
          <p class="text-sm text-gray-300">Gợi ý thông minh từ AI</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function startGame() {
  router.push('/game')
}

function goToLeaderboard() {
  router.push('/leaderboard')
}

function goToShop() {
  router.push('/shop')
}

function goToProfile() {
  router.push('/profile')
}
</script>

<style scoped>
.menu-button {
  position: relative;
  overflow: hidden;
}

.menu-button::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.menu-button:hover::before {
  width: 300px;
  height: 300px;
}

.feature-card {
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}
</style>
