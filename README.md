# 🐾 Pet-sitter Finder
**A full-stack web application for matching pet owners with trusted sitters.**

[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![GCP](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)](https://cloud.google.com/)
[![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white)](https://www.jenkins.io/)

## 🌟 Overview
**Pet-sitter Finder** เป็นแพลตฟอร์มเว็บแอปพลิเคชันที่ช่วยให้เจ้าของสัตว์เลี้ยงสามารถค้นหาและจองบริการพี่เลี้ยงสัตว์เลี้ยงได้อย่างสะดวกสบาย โปรเจกต์นี้เน้นการจัดการระบบสมาชิก การจอง (Booking) และการรีวิว โดยให้ความสำคัญกับการทำ **Containerization** และระบบ **CI/CD** เพื่อการ Deploy ที่มีประสิทธิภาพบนระบบคลาวด์ 

---

## 📸 User Interface
<p align="center">
  <img src="screenshots/search-page.png" width="400" alt="Search Sitter">
  <img src="screenshots/booking-detail.png" width="400" alt="Booking System">
</p>
<p align="center">
  <em>ตัวอย่างอินเทอร์เฟซการค้นหาพี่เลี้ยงสัตว์เลี้ยงและข้อมูลการจองที่ใช้งานง่ายและรวดเร็ว</em>
</p>

---

## ✨ Key Features
* **Pet-sitter Matching:** ค้นหาพี่เลี้ยงที่เหมาะสมพร้อมระบบกรองข้อมูลและดูโปรไฟล์ของผู้ให้บริการ.
* **Booking System:** ระบบจัดการการจองที่ซับซ้อน รองรับการบันทึกข้อมูลผู้ใช้ การจอง และการให้คะแนนรีวิว.
* **Scalable Backend:** พัฒนาด้วย Django REST Framework และใช้ PostgreSQL ในการบริหารจัดการฐานข้อมูลความสัมพันธ์ที่มีความซับซ้อน.
* **Modern Frontend:** พัฒนาด้วย Tailwind CSS เพื่อให้ได้ UI ที่ทันสมัยและรองรับการใช้งานผ่านมือถือ (Responsive Design).

## 🛠 DevOps & Cloud Deployment Highlights
* **Containerization:** **Containerized** แอปพลิเคชันด้วย **Docker** และ **Docker Compose** เพื่อให้มั่นใจว่าสภาพแวดล้อมในการพัฒนาและใช้งานจริงเหมือนกัน 100%.
* **Cloud Infrastructure:** **Deployed** ระบบบน **Google Cloud Platform (GCP)** และ **Configured** **Nginx** เป็น Reverse Proxy และ Load Balancer เพื่อบริหารจัดการ Traffic อย่างมีประสิทธิภาพ.
* **Automated Pipeline:** **Streamlined** กระบวนการพัฒนาด้วย **CI/CD Pipeline** ผ่าน **Jenkins** ร่วมกับ GitHub Webhooks เพื่อทำระบบ Build, Test และ Deployment อัตโนมัติเมื่อมีการ Update Code.

---

## 💻 Tech Stack
| Category | Technology Used |
| --- | --- |
| **Backend** | Django (Python)  |
| **Frontend** | Tailwind CSS, JavaScript, HTML  |
| **Database** | PostgreSQL  |
| **Infrastructure** | Docker, Docker Compose, Nginx  |
| **Cloud & CI/CD** | Google Cloud Platform (GCP), Jenkins  |
