# ✅ LINETOGEL — DAILY SEO CHECKLIST + CRON JOBS

---

## ⏰ CRON JOBS (Setup Sekali, Jalan Otomatis)

```bash
# Buka crontab
crontab -e

# Tambahkan 2 baris ini:
# 1. Daily Freshness — 2 AM WIB (19:00 UTC) setiap hari
0 19 * * * cd /root/.openclaw-autoclaw/workspace/linetogel && bash automation/daily-freshness.sh >> /tmp/linetogel-cron.log 2>&1

# 2. Weekly Full Audit — Senin 6 AM WIB (Minggu 23:00 UTC)
0 23 * * 0 cd /root/.openclaw-autoclaw/workspace/linetogel && python3 automation/system.py >> /tmp/linetogel-cron.log 2>&1

# Save & exit (:wq)
```

---

## 📋 DAILY CHECKLIST — 7 HARI

### 🌅 SETIAP PAGI (15 menit)

```
☐ Buka GSC → Performance → cek klik & impresi baru
☐ Buka GSC → Coverage → cek error/halaman tidak terindex
☐ Buka Analytics → Realtime → cek traffic sekarang
☐ Cek posisi keyword target di SERP (manual search)
☐ Balas komentar/mention di social media
```

### 📱 POSTING HARIAN (Rotasi Platform)

| Hari | Platform | Jam | Konten |
|------|----------|-----|--------|
| **Sen** | Twitter/X | 08:00 | Tips strategi + link artikel |
| **Sen** | Instagram | 12:00 | Infografis / statistik pasaran |
| **Sen** | Telegram | 20:00 | Jadwal result malam ini |
| **Sel** | Twitter/X | 08:00 | Testimoni member + CTA |
| **Sel** | TikTok | 18:00 | Video pendek (15-30 detik) |
| **Sel** | Telegram | 20:00 | Update result + tips |
| **Rab** | Twitter/X | 08:00 | Info pasaran / promo |
| **Rab** | Instagram | 12:00 | Carousel tips bermain |
| **Rab** | Telegram | 20:00 | Recap mingguan |
| **Kam** | Twitter/X | 08:00 | Fakta / statistik menarik |
| **Kam** | TikTok | 18:00 | Video edukasi |
| **Kam** | Telegram | 20:00 | Q&A session |
| **Jum** | Twitter/X | 08:00 | Weekend prep + strategi |
| **Jum** | Instagram | 12:00 | Reels — behind the scenes |
| **Jum** | Telegram | 20:00 | Jadwal weekend pasaran |
| **Sab** | Twitter/X | 10:00 | Poll: pasaran favorit |
| **Sab** | Instagram | 14:00 | Story: quiz interaktif |
| **Sab** | Telegram | 21:00 | Live result Hongkong |
| **Min** | Twitter/X | 10:00 | Weekly recap + stats |
| **Min** | Instagram | 16:00 | Infografis mingguan |
| **Min** | Telegram | 21:00 | Preview minggu depan |

### 📊 MINGGUAN (Setiap Minggu, 30 menit)

```
☐ Jalankan automation/system.py — cek skor & orphans
☐ Google Trends — cek tren keyword toto
☐ Kompetitor check — ada perubahan ranking?
☐ Update 1-2 artikel lama dengan data baru
☐ Cek broken links (GSC → Coverage)
☐ Review social media analytics
☐ Rencanakan konten minggu depan
```

### 📈 BULANAN (Awal Bulan, 1 jam)

```
☐ Full audit — semua halaman, schema, CWV
☐ Analisis GSC 30 hari — keyword naik/turun
☐ Analisis Analytics — traffic, bounce rate, konversi
☐ Analisis backlink — domain baru, anchor text, DR
☐ Update roadmap berdasarkan data
☐ Rapat strategi — apa yang berhasil, apa yang perlu diubah
☐ Content calendar bulan depan
☐ GBP — cek review baru, posting update
```

---

## 🚨 ALERT TRIGGERS (Segera Action!)

| Trigger | Action |
|---------|--------|
| **Traffic turun >20%** | Cek GSC manual actions, cek server, cek indexing |
| **Halaman deindex** | Request re-indexing via GSC, periksa konten |
| **Kompetitor baru rank 1** | Analisis strategi mereka, reverse engineer |
| **Backlink spam muncul** | Disavow via Google Disavow Tool |
| **Google algorithm update** | Pantau forum SEO, cek dampak ke site |

---

## 🔧 QUICK COMMANDS

```bash
# Cek status terbaru
cd /root/.openclaw-autoclaw/workspace/linetogel
python3 automation/system.py

# Manual freshness update
bash automation/daily-freshness.sh

# Deploy manual (kalau Vercel auto-deploy gagal)
git add -A && git commit -m "update" && git push origin main

# Cek sitemap
curl -s https://linetogel-pi.vercel.app/sitemap.xml | grep '<loc>' | wc -l

# Cek status HTTP semua halaman
curl -s -o /dev/null -w "%{http_code}" https://linetogel-pi.vercel.app/
```

---

*Generated: 2026-06-29 | Review: Every Monday*
