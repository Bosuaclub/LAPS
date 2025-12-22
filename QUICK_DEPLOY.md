# 🚀 Deploy FAO-Sim trong 5 phút

## ⚠️ QUAN TRỌNG

**Vercel chỉ hiển thị landing page hướng dẫn!**

Để sử dụng FAO-Sim thực sự, bạn cần deploy lên **Streamlit Cloud** (miễn phí).

---

## ✅ Bước 1: Deploy App Thật (Streamlit Cloud)

### 1.1. Truy cập Streamlit Cloud
Mở trình duyệt và vào: **https://share.streamlit.io**

### 1.2. Đăng nhập
Click **"Continue with GitHub"**

### 1.3. Tạo App Mới
Click **"New app"**

### 1.4. Cấu hình
Điền thông tin:
```
Repository: Bosuaclub/LAPS
Branch: claude/fb-ads-ai-optimization-Lgk6B
Main file path: faosim/ui/app.py
```

### 1.5. Thêm API Keys
Click **"Advanced settings"** → **"Secrets"**

Paste vào:
```toml
[openai]
api_key = "sk-proj-..."

[anthropic]
api_key = "sk-ant-..."
```

Thay `sk-proj-...` bằng API key thật của bạn.

### 1.6. Deploy
Click **"Deploy!"**

⏱️ Chờ 2-3 phút...

✅ **Done!** App của bạn sẽ live tại:
```
https://[tên-app-của-bạn].streamlit.app
```

---

## 📱 Bước 2: Lấy OpenAI API Key

Nếu chưa có API key:

1. Vào: **https://platform.openai.com/api-keys**
2. Click **"Create new secret key"**
3. Copy key (bắt đầu với `sk-proj-...`)
4. Paste vào Streamlit secrets (bước 1.5 ở trên)

---

## 🎯 Bước 3: Sử dụng App

Sau khi deploy thành công:

1. **Mở app URL**: `https://[your-app].streamlit.app`

2. **Vào tab "Configuration"**:
   - Chọn "Form Input"
   - Điền thông tin sản phẩm
   - Nhập dữ liệu lịch sử
   - Set mục tiêu (VD: ROAS 2.5)

3. **Vào tab "Run Optimization"**:
   - Review cấu hình
   - Click "Start Optimization"
   - Chờ 2-3 phút

4. **Xem kết quả** trong tab "Results"

---

## ❌ Tại sao không dùng Vercel?

Vercel **KHÔNG thể chạy Streamlit apps** vì:
- ❌ Serverless functions timeout sau 10-60 giây
- ❌ Không support WebSocket (Streamlit cần)
- ❌ Không có persistent state
- ❌ Không support long-running processes

**Vercel URL của bạn** chỉ hiển thị landing page hướng dẫn deploy đúng cách.

---

## 📊 So sánh

| Platform | App Thật? | Miễn phí? | Setup |
|----------|-----------|-----------|-------|
| **Streamlit Cloud** | ✅ YES | ✅ YES | 5 phút |
| Railway | ✅ YES | $5 credit | 10 phút |
| Render | ✅ YES | ✅ YES | 15 phút |
| **Vercel** | ❌ NO | N/A | Landing page only |

---

## 🆘 Gặp vấn đề?

### Lỗi: "Module not found"
**Fix**: Chờ deployment hoàn tất (2-3 phút)

### Lỗi: "Authentication Error"
**Fix**: Kiểm tra API key format trong secrets:
```toml
[openai]
api_key = "sk-proj-..."  # ✅ Đúng

openai_api_key = "..."    # ❌ Sai
```

### App chậm hoặc crash
**Fix**: Restart app trong Streamlit Cloud dashboard

### Không thấy app URL
**Fix**: Check email từ Streamlit Cloud hoặc vào dashboard

---

## 📚 Tài liệu chi tiết

- **STREAMLIT_CLOUD.md**: Hướng dẫn đầy đủ
- **DEPLOYMENT.md**: So sánh các platforms
- **docs/VERCEL_WHY_NOT.md**: Giải thích kỹ thuật

---

## ✅ Checklist

Deploy thành công khi:
- [ ] Vào được https://share.streamlit.io
- [ ] Đã connect GitHub account
- [ ] Chọn đúng repo: Bosuaclub/LAPS
- [ ] Main file: faosim/ui/app.py
- [ ] Đã thêm OpenAI API key
- [ ] Click Deploy thành công
- [ ] App hiển thị không lỗi

---

## 🎉 Kết quả mong đợi

Sau khi deploy xong, bạn sẽ có:

1. **URL app thật**: `https://[your-app].streamlit.app`
2. **Dashboard đầy đủ**: Configuration, Optimization, Results, Analytics
3. **Chạy được optimization**: Generate winning campaigns
4. **Download được kết quả**: JSON/CSV exports

**Không phải landing page!**

---

## 🚀 TL;DR (Tóm tắt)

```bash
# 1. Vào: https://share.streamlit.io
# 2. New app → Bosuaclub/LAPS → faosim/ui/app.py
# 3. Add OpenAI API key trong Secrets
# 4. Deploy!
#
# ✅ 5 phút = App thật chạy được
```

---

**Cần giúp?** Mở issue: https://github.com/Bosuaclub/LAPS/issues

**Version**: 1.0.0
**Last Updated**: 2025-12-22
