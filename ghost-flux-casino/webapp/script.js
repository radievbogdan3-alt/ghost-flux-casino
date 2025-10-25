class GhostFluxCasino {
    constructor() {
        this.userId = this.getUserId();
        this.balance = 0;
        this.inventory = [];
        this.isSpinning = false;
        
        this.init();
    }
    
    getUserId() {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('user_id');
    }
    
    async init() {
        await this.loadUserData();
        this.renderInventory();
        this.setupEventListeners();
        
        // Инициализация Telegram Web App
        if (window.Telegram && Telegram.WebApp) {
            Telegram.WebApp.ready();
            Telegram.WebApp.expand();
        }
    }
    
    async loadUserData() {
        // В реальном приложении здесь будет запрос к вашему бэкенду
        // Для демо используем localStorage
        const savedData = localStorage.getItem(`user_${this.userId}`);
        if (savedData) {
            const data = JSON.parse(savedData);
            this.balance = data.balance || 0;
            this.inventory = data.inventory || [];
        }
        this.updateBalance();
    }
    
    saveUserData() {
        localStorage.setItem(`user_${this.userId}`, JSON.stringify({
            balance: this.balance,
            inventory: this.inventory
        }));
    }
    
    updateBalance() {
        document.getElementById('balance').textContent = `Баланс: ${this.balance} ⭐`;
        const spinButton = document.getElementById('spinButton');
        
        if (this.balance < 50) {
            spinButton.classList.add('disabled');
            spinButton.textContent = 'Недостаточно звезд';
        } else {
            spinButton.classList.remove('disabled');
            spinButton.textContent = '🎰 Крутить за 50 ⭐';
        }
    }
    
    renderInventory() {
        const container = document.getElementById('inventoryItems');
        container.innerHTML = '';
        
        this.inventory.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.className = 'inventory-item';
            itemElement.innerHTML = `
                <div>${item.emoji}</div>
                <small>${item.name}</small>
            `;
            container.appendChild(itemElement);
        });
    }
    
    setupEventListeners() {
        document.getElementById('spinButton').addEventListener('click', () => this.spinRoulette());
        document.getElementById('withdrawBtn').addEventListener('click', () => this.withdrawPrizes());
        document.getElementById('depositBtn').addEventListener('click', () => this.depositBalance());
        document.getElementById('closeModal').addEventListener('click', () => this.closeModal());
    }
    
    async spinRoulette() {
        if (this.isSpinning || this.balance < 50) return;
        
        this.isSpinning = true;
        this.balance -= 50;
        this.updateBalance();
        
        const wheel = document.getElementById('rouletteWheel');
        const items = wheel.querySelectorAll('.roulette-item');
        
        // Анимация вращения
        wheel.classList.add('spinning');
        
        // Симуляция выбора приза (в реальном приложении - запрос к серверу)
        setTimeout(() => {
            const prize = this.getRandomPrize();
            this.showResult(prize);
            wheel.classList.remove('spinning');
            this.isSpinning = false;
        }, 3000);
    }
    
    getRandomPrize() {
        const prizes = [
            { name: "Мишка", value: 15, probability: 0.35, emoji: "🧸" },
            { name: "Сердечко", value: 15, probability: 0.35, emoji: "💖" },
            { name: "Ракета", value: 50, probability: 0.10, emoji: "🚀" },
            { name: "Торт", value: 50, probability: 0.10, emoji: "🎂" },
            { name: "Кубок", value: 100, probability: 0.05, emoji: "🏆" },
            { name: "Кольцо", value: 100, probability: 0.05, emoji: "💍" }
        ];
        
        const random = Math.random();
        let cumulative = 0;
        
        for (const prize of prizes) {
            cumulative += prize.probability;
            if (random <= cumulative) {
                return prize;
            }
        }
        
        return prizes[0];
    }
    
    showResult(prize) {
        this.inventory.push(prize);
        this.saveUserData();
        this.renderInventory();
        
        document.getElementById('resultTitle').textContent = 'Поздравляем! 🎉';
        document.getElementById('resultPrize').innerHTML = `
            <div style="font-size: 4em;">${prize.emoji}</div>
            <h3>${prize.name}</h3>
            <p>Ценность: ${prize.value} ⭐</p>
        `;
        
        document.getElementById('resultModal').style.display = 'block';
    }
    
    withdrawPrizes() {
        if (this.inventory.length === 0) {
            alert('🎒 Ваш инвентарь пуст!');
            return;
        }
        
        const totalValue = this.inventory.reduce((sum, item) => sum + item.value, 0);
        
        if (confirm(`Вы хотите вывести все призы общей стоимостью ${totalValue} звезд?`)) {
            // В реальном приложении здесь будет запрос к боту
            alert(`✅ Запрос на вывод отправлен администратору! Свяжитесь с @KXKXKXKXKXKXKXKXKXKXK`);
            this.inventory = [];
            this.saveUserData();
            this.renderInventory();
        }
    }
    
    depositBalance() {
        alert(`💰 Для пополнения баланса свяжитесь с администратором: @KXKXKXKXKXKXKXKXKXKXK\n\nМинимальное пополнение: 50 ⭐\nМаксимальное: 200 ⭐`);
    }
    
    closeModal() {
        document.getElementById('resultModal').style.display = 'none';
    }
}

// Запуск приложения
document.addEventListener('DOMContentLoaded', () => {
    new GhostFluxCasino();
});