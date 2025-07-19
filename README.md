# 📈 StockView API

**StockView** is a powerful FastAPI-based stock market analysis platform that brings together real-time stock prices, IPO tracking, mutual fund data, market news, and deep financial insights—all in one place.

From live price feeds to historical analytics, from IPO data to mutual fund insights—StockView delivers everything a modern investor or developer needs.

---

## 🚀 Key Features

- **🔴 Real-Time Stock Prices** – Live updates via WebSockets (every 5 seconds)
- **📊 Stock Analytics** – Historical trends, earnings, dividends & recommendations
- **🚀 IPO Dashboard** – Active, upcoming, listed & closed IPOs at a glance
- **📁 Mutual Funds** – Explore mutual funds across all categories
- **📰 Market News** – Latest headlines from top financial sources
- **📈 Interactive Charts** – Candlestick & moving average plots with Plotly
- **📈 Market Indices** – Real-time data on Nifty, Sensex & more

---

## 🛠️ Tech Stack

| Category         | Tools Used                                 |
|------------------|---------------------------------------------|
| **Backend**       | FastAPI (Python)                           |
| **Database**      | MongoDB                                    |
| **Auth**          | JWT + OTP via SendGrid                     |
| **Real-Time**     | WebSockets (5s interval updates)           |
| **Charts**        | Plotly, Matplotlib                         |
| **Email Service** | SendGrid                                   |
| **Data Sources**  | yFinance, News API, RapidAPI               |

---

## ⚡ Performance & Reliability

- **⏱️ Caching** – IPO and mutual fund data cached for 24 hours
- **📡 WebSocket Optimization** – Smooth and timely data streaming
- **🔍 Validation** – Pydantic models for clean input/output contracts
- **🧯 Robust Error Handling** – Descriptive, structured error responses

---

## 🔌 External Integrations

| Service         | Purpose                                      |
|------------------|----------------------------------------------|
| **Yahoo Finance** | Live stock prices, historical data          |
| **News API**      | Market and company-specific news            |
| **RapidAPI**      | Comprehensive IPO data                      |
| **SendGrid**      | Email service for OTP verification          |
| **Logo.dev**      | Fetch company logos for clean UI display    |

---
