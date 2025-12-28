# Game Specification: Đấu Trường Tri Thức
**Brain Arena: Only the Smart Survive**

## 1. Tổng Quan Dự Án

### 1.1 Mô Tả
Game "Đấu Trường Tri Thức" (Brain Arena: Only the Smart Survive) là game trắc nghiệm tri thức lấy cảm hứng từ chương trình "Ai Là Triệu Phú", nơi người chơi trả lời các câu hỏi với độ khó tăng dần để giành giải thưởng cao nhất và chứng minh trí tuệ của mình.

### 1.2 Mục Tiêu
- Tạo trải nghiệm chơi game hấp dẫn, giống chương trình truyền hình gốc
- Giao diện đẹp mắt, hiện đại với hiệu ứng âm thanh và hình ảnh sống động
- Hỗ trợ nhiều người chơi và lưu trữ kết quả

### 1.3 Nền Tảng
- **Web Application** (HTML, CSS, JavaScript)
- **Responsive Design** (hỗ trợ desktop, tablet, mobile)

---

## 2. AI Features 🤖

### 2.1 AI Question Generator (Tạo Câu Hỏi Tự Động)

#### Tính Năng
- **AI tự động sinh câu hỏi** dựa trên chủ đề và độ khó
- **Không bao giờ hết câu hỏi** - câu hỏi luôn mới mẻ
- **Đa dạng chủ đề**: Người chơi có thể chọn chủ đề yêu thích

#### Cơ Chế Hoạt Động
```javascript
// Sử dụng AI API (OpenAI, Gemini, Claude)
generateQuestion({
  level: 5,              // Câu số 5
  difficulty: "medium",  // Độ khó
  category: "Địa lý",    // Chủ đề
  language: "vi"         // Tiếng Việt
})
```

#### Output Mẫu
```json
{
  "question": "Sông nào dài nhất Việt Nam?",
  "answers": [
    {"id": "A", "text": "Sông Mekong", "correct": true},
    {"id": "B", "text": "Sông Hồng", "correct": false},
    {"id": "C", "text": "Sông Đồng Nai", "correct": false},
    {"id": "D", "text": "Sông Cửu Long", "correct": false}
  ],
  "explanation": "Sông Mekong dài 4.350km, trong đó 220km chảy qua Việt Nam",
  "source": "AI Generated"
}
```

#### Tùy Chọn Người Chơi
- **Chế độ AI**: Tất cả câu hỏi do AI tạo
- **Chế độ Hybrid**: Mix câu hỏi AI + câu hỏi có sẵn
- **Chế độ Classic**: Chỉ dùng câu hỏi có sẵn

### 2.2 AI Voice Narrator (Người Dẫn Chương Trình AI) 🎙️

#### Tính Năng
- **AI đọc câu hỏi và đáp án** bằng giọng nói tự nhiên
- **Text-to-Speech (TTS)** được train từ giọng thật
- **Đa dạng giọng**: Nam/Nữ, Miền Bắc/Nam/Trung

#### Giọng Miễn Phí (10 Giọng)

**Giọng Nam (5 giọng):**
1. **Nam Miền Bắc 1** - Giọng trầm, chuyên nghiệp
2. **Nam Miền Bắc 2** - Giọng trung, năng động
3. **Nam Miền Nam 1** - Giọng ấm, thân thiện
4. **Nam Miền Nam 2** - Giọng vui tươi
5. **Nam Miền Trung** - Giọng đặc trưng miền Trung

**Giọng Nữ (5 giọng):**
1. **Nữ Miền Bắc 1** - Giọng nhẹ nhàng, dịu dàng
2. **Nữ Miền Bắc 2** - Giọng rõ ràng, tự tin
3. **Nữ Miền Nam 1** - Giọng ngọt ngào
4. **Nữ Miền Nam 2** - Giọng sôi nổi
5. **Nữ Miền Trung** - Giọng đặc trưng miền Trung

#### Giọng Premium (VIP) 💎

**Giọng Người Nổi Tiếng** (Cần mua riêng hoặc VIP)
- **🌟 Giọng MC Lại Văn Sâm** - 50,000 VNĐ/tháng
  - Giọng chính thức của chương trình TV
  - Âm điệu đặc trưng, chuyên nghiệp
  
- **🎓 Giọng Giáo Sư Xoay** - 50,000 VNĐ/tháng
  - Giọng hài hước, gần gũi
  - Phù hợp cho chế độ vui vẻ

- **🎭 Giọng MC Phan Đăng** - 30,000 VNĐ/tháng
  - Giọng trẻ trung, năng động

- **👑 Gói VIP All Voices** - 100,000 VNĐ/tháng
  - Unlock tất cả giọng premium
  - Bao gồm: Unlimited AI Hint + AI Questions + No Ads

#### Cơ Chế Hoạt Động

```javascript
// AI Voice Service
class AIVoiceService {
  async readQuestion(text, voiceId) {
    // Sử dụng TTS API (Google Cloud TTS, ElevenLabs, hoặc custom)
    const audioUrl = await ttsAPI.synthesize({
      text: text,
      voiceId: voiceId,
      language: 'vi-VN',
      speed: 1.0,
      pitch: 0
    });
    
    return audioUrl;
  }
  
  async readAnswer(answerText, voiceId) {
    // Đọc từng đáp án A, B, C, D
    return await this.readQuestion(`Đáp án ${answerText}`, voiceId);
  }
}
```

#### Ví Dụ Kịch Bản Đọc

```
MC AI: "Câu hỏi số 5, trị giá 1 triệu đồng!"
[Pause 1s]
MC AI: "Thủ đô của Việt Nam là gì?"
[Pause 2s]
MC AI: "A - Hà Nội"
[Pause 1s]
MC AI: "B - Thành phố Hồ Chí Minh"
[Pause 1s]
MC AI: "C - Đà Nẵng"
[Pause 1s]
MC AI: "D - Huế"
[Pause 2s]
MC AI: "Bạn có 60 giây để trả lời. Chúc bạn may mắn!"
```

#### Tùy Chọn Người Chơi
- **Bật/Tắt** voice narrator
- **Chọn giọng** từ danh sách
- **Tốc độ đọc**: 0.8x, 1.0x, 1.2x
- **Auto-read**: Tự động đọc hoặc click để nghe
- **Volume**: Điều chỉnh âm lượng riêng cho voice



### 2.3 PvP Mode (Player vs Player) 🎮

#### Chế Độ Thi Đấu

**1. Real-time PvP**
- 2 người chơi cùng trả lời cùng lúc
- Ai nhanh + đúng hơn thắng
- Có thời gian giới hạn mỗi câu (30s)

**2. Async PvP (Turn-based)**
- Người chơi 1 chơi trước
- Kết quả được lưu lại
- Người chơi 2 thách đấu với kết quả đó

**3. Tournament Mode**
- Vòng loại: 16/32/64 người
- Đấu loại trực tiếp
- Người thắng vào vòng sau

#### Matchmaking System
```javascript
{
  "mode": "ranked",
  "criteria": {
    "skillLevel": "similar",    // Ghép người cùng trình độ
    "region": "Vietnam",         // Cùng khu vực (giảm lag)
    "waitTime": "< 30s"          // Thời gian chờ tối đa
  }
}
```

#### Ranking System 🏆

**Hệ Thống Xếp Hạng**
```
Hạng         | Điểm ELO    | Phần Thưởng
─────────────┼─────────────┼──────────────────
Đồng         | 0 - 999     | -
Bạc          | 1000 - 1499 | Badge Bạc
Vàng         | 1500 - 1999 | Badge Vàng + Avatar
Bạch Kim     | 2000 - 2499 | Badge + Avatar + Title
Kim Cương    | 2500 - 2999 | Tất cả + Skin đặc biệt
Cao Thủ      | 3000 - 3499 | Tất cả + Hiệu ứng đặc biệt
Huyền Thoại  | 3500+       | Tất cả + Tên trên Hall of Fame
```

**Tính Điểm ELO**
- Thắng: +20 đến +40 điểm (tùy đối thủ)
- Thua: -15 đến -30 điểm
- Hòa: ±5 điểm

#### Leaderboard (Bảng Xếp Hạng)

**All-Time Global Leaderboard**
- Top 100 người chơi toàn cầu
- Cập nhật real-time
- Hiển thị: Hạng, Tên, ELO, Win Rate, Số trận thắng
- Sắp xếp theo điểm ELO (cao nhất)


#### Profile & Stats
```javascript
{
  "username": "ProPlayer123",
  "level": 45,
  "elo": 2350,
  "rank": "Bạch Kim",
  "stats": {
    "totalGames": 150,
    "wins": 95,
    "losses": 55,
    "winRate": "63.3%",
    "highestScore": 85000000,
    "perfectGames": 12,        // Trả lời đúng 15/15
    "averageTime": "25s/câu"
  },
  "achievements": [
    "First Win",
    "10 Win Streak",
    "Speed Demon",
    "Perfect Game"
  ],
  "badges": ["🥈", "🏆", "⚡"],
  "title": "Bậc Thầy Tri Thức"
}
```

### 2.4 AI Chat Companion (Người Bạn Đồng Hành AI)

#### Tính Năng
- **AI Chatbot** luôn sẵn sàng trò chuyện
- Động viên khi thua, chúc mừng khi thắng
- Giải thích đáp án sau mỗi câu hỏi
- Gợi ý chiến lược chơi

#### Ví Dụ Tương Tác
```
[Sau khi trả lời đúng câu 10]
AI: "Xuất sắc! Bạn đã vượt qua mốc 14 triệu! 
     Bạn có muốn tôi giải thích tại sao đáp án 
     B đúng không?"

[Khi người chơi do dự]
AI: "Bạn còn 2 quyền trợ giúp. Câu này khá khó, 
     có thể dùng AI Hint nhé!"

[Khi thua]
AI: "Đừng buồn! Bạn đã làm rất tốt. Lần sau 
     hãy thử chế độ AI Dễ để luyện tập nhé!"
```

---

## 3. Gameplay & Cơ Chế

### 2.1 Luật Chơi Cơ Bản

#### Cấu Trúc Câu Hỏi
- **15 câu hỏi** với độ khó tăng dần
- **4 đáp án** cho mỗi câu hỏi (A, B, C, D)
- **1 đáp án đúng** duy nhất

#### Thang Điểm/Giải Thưởng
```
Câu 15: 150,000,000 VNĐ (Triệu Phú) 🏆
Câu 14: 85,000,000 VNĐ
Câu 13: 60,000,000 VNĐ
Câu 12: 40,000,000 VNĐ
Câu 11: 22,000,000 VNĐ
Câu 10: 14,000,000 VNĐ (Mốc an toàn 2) 💰
Câu 9:  10,000,000 VNĐ
Câu 8:  6,000,000 VNĐ
Câu 7:  3,000,000 VNĐ
Câu 6:  2,000,000 VNĐ
Câu 5:  1,000,000 VNĐ (Mốc an toàn 1) 💰
Câu 4:  600,000 VNĐ
Câu 3:  400,000 VNĐ
Câu 2:  200,000 VNĐ
Câu 1:  100,000 VNĐ
```

#### Mốc An Toàn
- **Mốc 1**: Câu 5 (1,000,000 VNĐ)
- **Mốc 2**: Câu 10 (14,000,000 VNĐ)
- Khi trả lời sai sau khi vượt mốc an toàn, người chơi về mốc đó (không về 0)

### 2.2 Quyền Trợ Giúp

#### Quyền Miễn Phí (3 Quyền)

**1. 50:50 (Loại Bỏ 2 Đáp Án)** ⚡
- **Mô tả**: Loại bỏ 2 đáp án sai, chỉ còn lại 2 đáp án (1 đúng, 1 sai)
- **Số lần sử dụng**: 1 lần/game
- **Hiệu ứng**: 2 đáp án sai mờ đi/ẩn đi với animation
- **Icon**: ⚡ hoặc 50/50

**2. Time Freeze (Dừng Thời Gian)** ⏸️
- **Mô tả**: Dừng đồng hồ đếm ngược thêm 30 giây để suy nghĩ
- **Số lần sử dụng**: 1 lần/game
- **Áp dụng**: Chỉ khi có giới hạn thời gian
- **Hiệu ứng**: Đồng hồ đóng băng với animation
- **Icon**: ⏸️ hoặc ❄️

**3. Swap Question (Đổi Câu Hỏi)** 🔄
- **Mô tả**: Đổi sang câu hỏi khác cùng độ khó
- **Số lần sử dụng**: 1 lần/game
- **Lưu ý**: Vẫn giữ nguyên số tiền hiện tại
- **Điều kiện**: Không áp dụng cho câu 15 (câu cuối)
- **Icon**: 🔄 hoặc ⏭️

---

#### Quyền Premium (Cần Nạp Tiền) 💎

**4. AI Hint (Gợi Ý Thông Minh)** 🤖
- **Mô tả**: AI phân tích câu hỏi và đưa ra gợi ý thông minh
- **Số lần sử dụng**: 
  - **Gói Basic**: 3 lần AI Hint - 10,000 VNĐ
  - **Gói Pro**: 10 lần AI Hint - 30,000 VNĐ
  - **Gói VIP**: Unlimited AI Hint - 50,000 VNĐ/tháng
- **Output**:
  - Loại bỏ 1 đáp án sai chắc chắn
  - Giải thích ngắn gọn (1-2 câu)
  - Độ tin cậy (70-95%)
- **Ví dụ**: 
  ```
  AI Hint: "Đáp án C có thể loại bỏ vì không phù hợp 
  với bối cảnh lịch sử. Tôi tin 85% đáp án đúng là B."
  ```
- **Icon**: 🤖 hoặc 💡
- **Lưu ý**: Có thể mua thêm lượt sử dụng trong game

### 2.3 Tính Năng Dừng Chơi
- Người chơi có thể **dừng chơi** bất kỳ lúc nào
- Nhận số tiền tương ứng với câu hỏi hiện tại
- Hiển thị xác nhận trước khi dừng

---

## 3. Giao Diện Người Dùng (UI/UX)

### 3.1 Màn Hình Chính (Home Screen)

#### Thành Phần
- **Logo game** lớn, nổi bật
- **Nút "Chơi Ngay"** (Play Now)
- **Nút "Bảng Xếp Hạng"** (Leaderboard)
- **Nút "Cài Đặt"** (Settings)
- **Nút "Hướng Dẫn"** (How to Play)

#### Thiết Kế
- Background gradient tím-xanh hoặc vàng-cam (giống chương trình TV)
- Hiệu ứng ánh sáng lấp lánh
- Âm nhạc nền (có thể tắt)

### 3.2 Màn Hình Chơi Game (Game Screen)

#### Layout
```
┌─────────────────────────────────────────┐
│         [Thang Điểm - Bên Phải]         │
│  ┌───────────────────────────────────┐  │
│  │     Câu Hỏi Số X - XXX,XXX VNĐ    │  │
│  │                                   │  │
│  │  Nội dung câu hỏi ở đây...        │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌─────────┐  ┌─────────┐              │
│  │  A: ...  │  │  B: ...  │              │
│  └─────────┘  └─────────┘              │
│  ┌─────────┐  ┌─────────┐              │
│  │  C: ...  │  │  D: ...  │              │
│  └─────────┘  └─────────┘              │
│                                         │
│  [50:50] [⏸️ Dừng] [🔄 Swap] [🤖 AI 💎]  │
└─────────────────────────────────────────┘
```

#### Thành Phần Chi Tiết

**1. Thang Điểm (Money Ladder)**
- Hiển thị cố định bên phải màn hình
- Câu hỏi hiện tại được highlight (màu vàng/cam)
- Mốc an toàn có icon đặc biệt (💰)
- Các câu đã vượt qua: màu xanh lá
- Các câu chưa đến: màu xám

**2. Khu Vực Câu Hỏi**
- Background tối, text sáng
- Font chữ lớn, dễ đọc
- Số câu hỏi và giá trị tiền thưởng hiển thị rõ ràng
- Có thể có hình ảnh minh họa (tùy câu hỏi)

**3. Khu Vực Đáp Án**
- 4 nút lớn, rõ ràng (A, B, C, D)
- Hiệu ứng hover khi di chuột
- Hiệu ứng click: đáp án được chọn sáng lên
- Animation khi công bố đáp án:
  - Đúng: màu xanh lá, hiệu ứng sáng
  - Sai: màu đỏ, rung nhẹ
  - Đáp án đúng sẽ sáng xanh sau khi chọn sai

**4. Thanh Quyền Trợ Giúp**
- 4 nút icon rõ ràng
- Nút đã sử dụng: mờ đi, không click được
- Tooltip khi hover để giải thích
- Animation khi sử dụng

**5. Nút Dừng Chơi**
- Nút riêng biệt, màu cam/vàng
- Hiển thị popup xác nhận khi click

### 3.3 Màn Hình Kết Quả (Result Screen)

#### Thành Phần
- **Thông báo kết quả**: "Chúc mừng!" hoặc "Rất tiếc!"
- **Số tiền giành được**: Hiển thị lớn, nổi bật
- **Thống kê**:
  - Số câu trả lời đúng
  - Quyền trợ giúp đã sử dụng
  - Thời gian chơi
- **Nút "Chơi Lại"**
- **Nút "Về Trang Chủ"**
- **Nút "Xem Bảng Xếp Hạng"**

#### Hiệu Ứng
- Pháo hoa nếu thắng lớn (>= 14,000,000)
- Confetti nếu đạt mốc an toàn
- Animation số tiền tăng dần

### 3.4 Bảng Xếp Hạng (Leaderboard)

#### Thông Tin Hiển Thị
- **Top 100 người chơi toàn cầu** (all-time)
- Thông tin mỗi người:
  - Hạng
  - Tên người chơi
  - Điểm ELO
  - Win Rate (% thắng)
  - Số trận thắng
  - Ngày tham gia

#### Tính Năng
- Sắp xếp theo ELO (cao nhất)
- Highlight người chơi hiện tại
- Search theo tên người chơi
- Xem vị trí của bản thân

### 3.5 Màn Hình Cài Đặt (Settings)

#### Tùy Chọn
- **Âm thanh**:
  - Nhạc nền (On/Off, Volume)
  - Hiệu ứng âm thanh (On/Off, Volume)
  - **AI Voice Narrator** 🎙️:
    - Bật/Tắt người dẫn AI
    - Chọn giọng (10 giọng miễn phí)
    - Tốc độ đọc (0.8x, 1.0x, 1.2x)
    - Auto-read (Tự động/Click để nghe)
    - Volume riêng cho voice
- **Độ khó**:
  - Dễ (câu hỏi dễ hơn)
  - Trung bình
  - Khó (câu hỏi khó hơn)
- **Thời gian suy nghĩ**:
  - Không giới hạn
  - 60 giây/câu
  - 45 giây/câu
  - 30 giây/câu
- **Quyền trợ giúp miễn phí**:
  - Bật/tắt: 50:50, Time Freeze, Swap Question
- **Quyền trợ giúp Premium** 💎:
  - Xem gói AI Hint đã mua
  - Mua thêm lượt AI Hint
  - Nút "Nâng Cấp Premium"
- **Chế độ câu hỏi**:
  - Classic (câu hỏi có sẵn)
  - AI Generated (AI tạo câu hỏi) 💎
  - Hybrid (mix cả hai) 💎
- **Ngôn ngữ**: Tiếng Việt (mặc định)

---

### 3.6 Màn Hình Shop (In-App Purchase) 💎

#### Gói AI Hint
```
┌─────────────────────────────────┐
│   🤖 AI HINT PACKAGES           │
├─────────────────────────────────┤
│ ⚡ BASIC                         │
│ 3 lần AI Hint                   │
│ 10,000 VNĐ                      │
│ [MUA NGAY]                      │
├─────────────────────────────────┤
│ 🔥 PRO (Phổ biến)               │
│ 10 lần AI Hint                  │
│ 30,000 VNĐ (Tiết kiệm 25%)     │
│ [MUA NGAY]                      │
├─────────────────────────────────┤
│ 👑 VIP                          │
│ Unlimited AI Hint               │
│ 50,000 VNĐ/tháng                │
│ + AI Generated Questions        │
│ + Không quảng cáo               │
│ [MUA NGAY]                      │
└─────────────────────────────────┘
```

#### Gói Giọng Premium 🎙️
```
┌─────────────────────────────────┐
│   🎙️ PREMIUM VOICES             │
├─────────────────────────────────┤
│ 🌟 MC Lại Văn Sâm               │
│ Giọng chính thức, chuyên nghiệp │
│ 50,000 VNĐ/tháng                │
│ [MUA NGAY]                      │
├─────────────────────────────────┤
│ 🎓 Giáo Sư Xoay                 │
│ Giọng hài hước, gần gũi         │
│ 50,000 VNĐ/tháng                │
│ [MUA NGAY]                      │
├─────────────────────────────────┤
│ 🎭 MC Phan Đăng                 │
│ Giọng trẻ trung, năng động      │
│ 30,000 VNĐ/tháng                │
│ [MUA NGAY]                      │
├─────────────────────────────────┤
│ 👑 VIP ALL-IN-ONE               │
│ • Unlimited AI Hint             │
│ • AI Generated Questions        │
│ • All Premium Voices            │
│ • Không quảng cáo               │
│ 100,000 VNĐ/tháng               │
│ [MUA NGAY] ⭐ Best Value        │
└─────────────────────────────────┘
```

#### Phương Thức Thanh Toán
- Thẻ ATM/Visa/Mastercard
- Ví điện tử (MoMo, ZaloPay, VNPay)
- Chuyển khoản ngân hàng
- Google Play / App Store (nếu có app)

---

## 4. Hệ Thống Câu Hỏi

### 4.1 Cấu Trúc Dữ Liệu Câu Hỏi

```json
{
  "id": "Q001",
  "question": "Thủ đô của Việt Nam là gì?",
  "answers": [
    {"id": "A", "text": "Hà Nội", "correct": true},
    {"id": "B", "text": "Hồ Chí Minh", "correct": false},
    {"id": "C", "text": "Đà Nẵng", "correct": false},
    {"id": "D", "text": "Huế", "correct": false}
  ],
  "level": 1,
  "category": "Địa lý",
  "difficulty": "easy",
  "image": null
}
```

### 4.2 Phân Loại Câu Hỏi

#### Theo Độ Khó
- **Dễ** (Câu 1-5): Kiến thức phổ thông, thường thức
- **Trung bình** (Câu 6-10): Kiến thức chuyên sâu hơn
- **Khó** (Câu 11-15): Kiến thức chuyên môn, ít phổ biến

#### Theo Chủ Đề
- Địa lý
- Lịch sử
- Văn học
- Khoa học
- Thể thao
- Giải trí
- Công nghệ
- Toán học
- Nghệ thuật
- Thường thức

### 4.3 Yêu Cầu Ngân Hàng Câu Hỏi
- **Tối thiểu**: 150 câu (10 bộ câu hỏi hoàn chỉnh)
- **Khuyến nghị**: 500+ câu để tránh lặp lại
- **Cập nhật**: Thêm câu hỏi mới định kỳ

---

## 5. Technical Implementation

> **📄 Chi tiết kỹ thuật đầy đủ xem tại: [TECHNICAL_DOCS.md](./TECHNICAL_DOCS.md)**

### Tech Stack Summary
- **Backend**: Python + FastAPI
- **Database**: MySQL 8.0+ + Redis
- **AI**: Google Gemini API + VieNeu-TTS
- **Frontend**: React/Vue.js + WebSocket

---

## 6. Hiệu Ứng & Animation

### 6.1 Hiệu Ứng Hình Ảnh

#### Transition Câu Hỏi
- Fade out câu cũ
- Fade in câu mới
- Duration: 0.5s

#### Hiệu Ứng Đáp Án
- **Hover**: Scale 1.05, shadow tăng
- **Click**: Pulse effect
- **Đúng**: Glow xanh lá, confetti nhỏ
- **Sai**: Shake effect, flash đỏ

#### Hiệu Ứng Quyền Trợ Giúp
- **50:50**: 2 đáp án sai fade out
- **Khán giả**: Bar chart animate từ 0 đến %
- **Gọi điện**: Typing effect cho text

### 6.2 Hiệu Ứng Âm Thanh

#### Âm Thanh Chính
- **Nhạc nền**: Loop, thay đổi theo mức độ căng thẳng
- **Chọn đáp án**: Click sound
- **Đúng**: Ding! + nhạc vui
- **Sai**: Buzzer + nhạc buồn
- **Quyền trợ giúp**: Whoosh sound
- **Thắng lớn**: Fanfare

---

## 7. Roadmap Phát Triển

### Phase 1: MVP (Minimum Viable Product) - 2-3 tuần
**Mục tiêu**: Game cơ bản có thể chơi được

- [ ] **Frontend Core**
  - [ ] Giao diện cơ bản (Home, Game, Result)
  - [ ] Logic game cơ bản (15 câu hỏi, 4 đáp án)
  - [ ] 2 quyền trợ giúp cơ bản: 50:50, Time Freeze
  - [ ] Responsive design cơ bản
  
- [ ] **Content**
  - [ ] 50 câu hỏi mẫu (manual)
  - [ ] Âm thanh cơ bản
  
- [ ] **Data**
  - [ ] LocalStorage để lưu high score
  - [ ] Settings cơ bản

**Deliverable**: Game đơn giản có thể chơi offline

---

### Phase 2: Enhanced Features + AI Integration - 3-4 tuần
**Mục tiêu**: Thêm tính năng nâng cao và AI cơ bản

- [ ] **Game Features**
  - [ ] Thêm quyền trợ giúp: Swap Question
  - [ ] Bảng xếp hạng local
  - [ ] Animation mượt mà
  - [ ] 200+ câu hỏi manual
  - [ ] Hệ thống thời gian đếm ngược (cho Time Freeze)
  
- [ ] **AI Features - Basic**
  - [ ] Tích hợp Gemini API
  - [ ] AI Question Generator (chế độ AI)
  - [ ] Chế độ Hybrid (mix AI + manual questions)
  - [ ] AI Voice Narrator (10 giọng miễn phí)
  - [ ] Text-to-Speech integration
  
- [ ] **Backend Setup**
  - [ ] Node.js + Express server
  - [ ] PostgreSQL database
  - [ ] User authentication (register/login)
  - [ ] Basic API endpoints
  - [ ] Payment gateway integration (MoMo/ZaloPay/VNPay)
  - [ ] Shop system (AI Hint packages)

**Deliverable**: Game với AI tạo câu hỏi tự động + Shop system

---

### Phase 3: Advanced AI + PvP - 4-5 tuần
**Mục tiêu**: PvP mode và AI nâng cao

- [ ] **AI Features - Advanced**
  - [ ] AI Hint optimization (cải thiện độ chính xác)
  - [ ] AI Chat Companion (beta)
  - [ ] AI difficulty adjustment (điều chỉnh độ khó tự động)
  - [ ] Premium Voices (MC Lại Văn Sâm, Giáo Sư Xoay, etc.)
  - [ ] Voice cloning quality improvement
  
- [ ] **PvP Mode**
  - [ ] WebSocket server setup
  - [ ] Real-time PvP (1v1)
  - [ ] Async PvP (turn-based)
  - [ ] Matchmaking system
  
- [ ] **Ranking System**
  - [ ] ELO rating calculation
  - [ ] Hệ thống hạng (Đồng → Huyền Thoại)
  - [ ] Global leaderboard (all-time)
  
- [ ] **User Profile**
  - [ ] Profile page với stats
  - [ ] Achievements system
  - [ ] Badges & Titles
  - [ ] Avatar upload

**Deliverable**: Game multiplayer với ranking system hoàn chỉnh

---

### Phase 4: Polish + Advanced Features - 3-4 tuần
**Mục tiêu**: Hoàn thiện và tối ưu

- [ ] **Advanced Features**
  - [ ] Tournament mode (16/32/64 người)
  - [ ] Friends system
  - [ ] Challenge friends
  - [ ] Chia sẻ kết quả lên mạng xã hội
  
- [ ] **AI Enhancements**
  - [ ] AI Chat Companion (full version)
  - [ ] AI giải thích đáp án
  - [ ] AI phân tích điểm mạnh/yếu của người chơi
  - [ ] Personalized question recommendations
  
- [ ] **Performance & Optimization**
  - [ ] Redis caching
  - [ ] CDN setup
  - [ ] Database optimization
  - [ ] AI cost optimization
  - [ ] Load testing
  
- [ ] **Polish**
  - [ ] Premium UI/UX
  - [ ] Advanced animations
  - [ ] Sound effects đầy đủ
  - [ ] Mobile app (PWA)

**Deliverable**: Game production-ready với tất cả tính năng

---

### Phase 5: Monetization & Growth (Optional) - Ongoing
**Mục tiêu**: Tối ưu doanh thu

- [ ] **Monetization**
  - [ ] AI Hint packages (chính) 💎
    - [ ] Gói Basic: 10,000 VNĐ
    - [ ] Gói Pro: 30,000 VNĐ
    - [ ] Gói VIP: 50,000 VNĐ/tháng
  - [ ] Premium Voices 🎙️
    - [ ] MC Lại Văn Sâm: 50,000 VNĐ/tháng
    - [ ] Giáo Sư Xoay: 50,000 VNĐ/tháng
    - [ ] MC Phan Đăng: 30,000 VNĐ/tháng
  - [ ] VIP All-in-One: 100,000 VNĐ/tháng
  - [ ] AI Generated Questions (VIP only)
  - [ ] Quảng cáo (cho free users, tắt được khi mua VIP)
  - [ ] Tournament entry fees (tùy chọn)
  - [ ] Cosmetics (avatars, badges, themes)
  
- [ ] **Growth Features**
  - [ ] Referral system (tặng 1 lượt AI Hint khi mời bạn)
  - [ ] Daily rewards (login hàng ngày)
  - [ ] Free AI Hint mỗi ngày (1 lượt)
  - [ ] Seasonal events
  - [ ] Special tournaments
  - [ ] Influencer partnerships
  
- [ ] **Analytics & Optimization**
  - [ ] Google Analytics
  - [ ] Payment conversion tracking
  - [ ] A/B testing (giá gói, UI shop)
  - [ ] User behavior analysis
  - [ ] Churn rate monitoring

**Deliverable**: Sustainable revenue stream từ AI Hint premium

---

### Timeline Summary
```
Phase 1 (MVP):              ████████░░░░░░░░░░░░  (2-3 tuần)
Phase 2 (AI Basic):         ░░░░░░░░██████░░░░░░  (3-4 tuần)
Phase 3 (PvP + Ranking):    ░░░░░░░░░░░░░░████░░  (4-5 tuần)
Phase 4 (Polish):           ░░░░░░░░░░░░░░░░░░██  (3-4 tuần)
─────────────────────────────────────────────────
Total:                      12-16 tuần (~3-4 tháng)
```

### Resource Requirements

**Development Team** (Recommended)
- 1 Frontend Developer
- 1 Backend Developer
- 1 AI/ML Engineer (part-time)
- 1 UI/UX Designer (part-time)
- 1 QA Tester (part-time)

**Infrastructure Costs** (Monthly estimate)
- **Hosting**: $20-50 (Vercel/Railway/DigitalOcean)
- **Database**: $15-30 (PostgreSQL + Redis)
- **AI API**: $50-200 (Gemini API - depends on usage)
- **TTS API**: $30-100 (Google Cloud TTS / ElevenLabs)
- **CDN**: $10-20 (Cloudflare/BunnyCDN)
- **Payment Gateway**: 2-3% per transaction (MoMo/ZaloPay/VNPay)
- **Total Fixed**: ~$130-400/month
- **Total Variable**: Phụ thuộc vào số lượng giao dịch

**Revenue Projection** (Conservative estimate)
- 1000 users/month
- 15% conversion rate = 150 buyers
  - 100 mua AI Hint (avg 30k VNĐ) = 3,000,000 VNĐ
  - 50 mua Premium Voice (avg 40k VNĐ) = 2,000,000 VNĐ
- Monthly revenue: 5,000,000 VNĐ (~$200)
- Profit margin: 60-70% (sau khi trừ chi phí)
- Net profit: ~$120-140/month

**AI API Cost Optimization**
- Cache questions aggressively
- Use AI only when needed (not for every game)
- Implement daily limits per user
- Offer "Classic mode" (no AI) as default



---

## 8. Wireframes & Mockups

### 8.1 Home Screen Wireframe
```
┌────────────────────────────────────┐
│                                    │
│    🏆 AI LÀ TRIỆU PHÚ 🏆          │
│                                    │
│         [CHƠI NGAY]                │
│                                    │
│      [Bảng Xếp Hạng]               │
│      [Hướng Dẫn]                   │
│      [Cài Đặt]                     │
│                                    │
│      © 2025 - Version 1.0          │
└────────────────────────────────────┘
```

### 8.2 Game Screen Wireframe
```
┌────────────────────────────────────────────────┐
│  Câu 5 - 1,000,000 VNĐ          │ 15: 150tr   │
│                                  │ 14: 85tr    │
│  ┌────────────────────────────┐  │ 13: 60tr    │
│  │ Thủ đô của Việt Nam là gì? │  │ 12: 40tr    │
│  └────────────────────────────┘  │ 11: 22tr    │
│                                  │ 10: 14tr 💰 │
│  ┌──────────┐  ┌──────────┐     │ 9:  10tr    │
│  │ A: Hà Nội │  │ B: TP.HCM│     │ 8:  6tr     │
│  └──────────┘  └──────────┘     │ 7:  3tr     │
│  ┌──────────┐  ┌──────────┐     │ 6:  2tr     │
│  │ C: Đà Nẵng│  │ D: Huế   │     │►5:  1tr 💰  │
│  └──────────┘  └──────────┘     │ 4:  600k    │
│                                  │ 3:  400k    │
│  [50:50] [👥] [📞] [⏸ DỪNG]     │ 2:  200k    │
│                                  │ 1:  100k    │
└────────────────────────────────────────────────┘
```

---

## 9. Testing & Quality Assurance

### 9.1 Test Cases

#### Functional Testing
- [ ] Tất cả 15 câu hỏi hiển thị đúng
- [ ] Chọn đáp án đúng → Tiến lên câu tiếp theo
- [ ] Chọn đáp án sai → Game over hoặc về mốc an toàn
- [ ] Mỗi quyền trợ giúp chỉ dùng được 1 lần
- [ ] 50:50 loại đúng 2 đáp án sai
- [ ] Dừng chơi → Nhận tiền đúng
- [ ] Leaderboard cập nhật đúng
- [ ] Settings lưu và áp dụng đúng

#### UI/UX Testing
- [ ] Responsive trên mobile, tablet, desktop
- [ ] Tất cả button có hover effect
- [ ] Animation mượt mà, không lag
- [ ] Font chữ rõ ràng, dễ đọc
- [ ] Màu sắc hài hòa, không chói mắt

#### Performance Testing
- [ ] Load time < 3 giây
- [ ] Smooth animation (60fps)
- [ ] Âm thanh không bị delay
- [ ] Không memory leak

### 9.2 Browser Compatibility
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

---

## 10. Launch Checklist

### Pre-Launch
- [ ] Hoàn thành tất cả tính năng Phase 1
- [ ] Test trên tất cả browsers
- [ ] Test trên mobile devices
- [ ] Chuẩn bị ít nhất 100 câu hỏi
- [ ] Tối ưu hóa performance
- [ ] Viết documentation

### Launch
- [ ] Deploy lên hosting (Vercel, Netlify, etc.)
- [ ] Setup domain (nếu có)
- [ ] Setup analytics (Google Analytics)
- [ ] Tạo landing page
- [ ] Chuẩn bị social media posts

### Post-Launch
- [ ] Monitor user feedback
- [ ] Fix bugs nhanh chóng
- [ ] Thêm câu hỏi mới hàng tuần
- [ ] Cập nhật features dựa trên feedback
- [ ] Marketing và promotion

---

## 11. Tài Liệu Tham Khảo

### Design Inspiration
- Chương trình "Ai Là Triệu Phú" trên VTV
- "Who Wants to Be a Millionaire" (bản quốc tế)
- Các game quiz online tương tự

### Technical Resources
- MDN Web Docs (HTML, CSS, JavaScript)
- Howler.js documentation (Audio)
- LocalStorage API
- CSS Animation tutorials

---

## 12. Liên Hệ & Support

### Phát Triển
- **Developer**: [Tên của bạn]
- **Email**: [Email của bạn]
- **GitHub**: [Link repository]

### Feedback
- Báo lỗi: [Link form hoặc email]
- Đề xuất tính năng: [Link form]
- Đóng góp câu hỏi: [Link form]

---

**Version**: 1.0  
**Last Updated**: 2025-12-28  
**Status**: Draft - Ready for Development

