import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import random
from datetime import datetime
import openai

st.set_page_config(
    page_title="MindfulStudy Hub",
    page_icon="🧘‍♀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<script>
function triggerBadgeCelebration(badgeName, badgeEmoji) {
    console.log('Triggering badge celebration:', badgeName, badgeEmoji);
    
    // Find the badge element and make it jiggle
    const badges = document.querySelectorAll('.badge');
    badges.forEach(badge => {
        if (badge.textContent.includes(badgeEmoji)) {
            badge.style.animation = 'badgeJiggle 2s ease-in-out';
            badge.style.transform = 'scale(1.5)';
            
            // Reset after animation
            setTimeout(() => {
                badge.style.animation = '';
                badge.style.transform = '';
            }, 2000);
        }
    });
}

function showBadgeOverview(badgeName, badgeEmoji, description, requirement) {
    // Create overlay
    const overlay = document.createElement('div');
    overlay.id = 'badge-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
        animation: fadeIn 0.3s ease-out;
    `;
    
    // Create badge overview card
    const card = document.createElement('div');
    card.style.cssText = `
        background: linear-gradient(135deg, #4ade80, #60a5fa, #f97316);
        padding: 40px;
        border-radius: 25px;
        text-align: center;
        color: white;
        max-width: 400px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        animation: badgeOverviewPop 0.5s ease-out;
        position: relative;
        overflow: hidden;
    `;
    
    // Add animated background
    const bgAnimation = document.createElement('div');
    bgAnimation.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%);
        animation: shimmer 2s infinite;
        z-index: 0;
    `;
    
    // Badge content
    const content = document.createElement('div');
    content.style.cssText = `
        position: relative;
        z-index: 1;
    `;
    content.innerHTML = `
        <div style="font-size: 4rem; margin-bottom: 20px; animation: badgeSpin 2s ease-in-out infinite;">${badgeEmoji}</div>
        <div style="font-size: 1.8rem; font-weight: bold; margin-bottom: 15px; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);">${badgeName}</div>
        <div style="font-size: 1.1rem; margin-bottom: 20px; line-height: 1.5; opacity: 0.9;">${description}</div>
        <div style="font-size: 1rem; opacity: 0.8; font-style: italic;">${requirement}</div>
        <div style="margin-top: 25px;">
            <button onclick="closeBadgeOverview()" style="
                background: rgba(255, 255, 255, 0.2);
                border: 2px solid white;
                color: white;
                padding: 10px 25px;
                border-radius: 20px;
                font-size: 1rem;
                cursor: pointer;
                transition: all 0.3s ease;
            " onmouseover="this.style.background='rgba(255, 255, 255, 0.3)'" onmouseout="this.style.background='rgba(255, 255, 255, 0.2)'">
                ✨ Awesome!
            </button>
        </div>
    `;
    
    card.appendChild(bgAnimation);
    card.appendChild(content);
    overlay.appendChild(card);
    document.body.appendChild(overlay);
    
    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes badgeOverviewPop {
            0% { transform: scale(0.5) rotate(-10deg); opacity: 0; }
            50% { transform: scale(1.1) rotate(5deg); }
            100% { transform: scale(1) rotate(0deg); opacity: 1; }
        }
        
        @keyframes badgeSpin {
            0%, 100% { transform: rotate(0deg) scale(1); }
            25% { transform: rotate(5deg) scale(1.1); }
            75% { transform: rotate(-5deg) scale(1.1); }
        }
        
        @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
        }
    `;
    document.head.appendChild(style);
}

function closeBadgeOverview() {
    const overlay = document.getElementById('badge-overlay');
    if (overlay) {
        overlay.style.animation = 'fadeOut 0.3s ease-out forwards';
        setTimeout(() => {
            overlay.remove();
        }, 300);
    }
}

// Make functions globally available
window.triggerBadgeCelebration = triggerBadgeCelebration;
window.showBadgeOverview = showBadgeOverview;
window.closeBadgeOverview = closeBadgeOverview;
</script>
""", unsafe_allow_html=True)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One:wght@400&family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Fun Color Palette */
    :root {
        --primary-blue: #58cc02;
        --primary-green: #58cc02;
        --primary-yellow: #ffc800;
        --primary-orange: #ff9600;
        --primary-red: #ff4b4b;
        --primary-purple: #ce82ff;
        --primary-pink: #ff6b9d;
        --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --card-bg: rgba(255, 255, 255, 0.95);
        --text-dark: #2d3748;
        --text-light: #4a5568;
        --shadow-color: rgba(0, 0, 0, 0.1);
        --border-radius: 20px;
    }
    
    /* Fun animated background */
    .stApp[data-testid="stAppViewContainer"] {
        background: linear-gradient(-45deg, #667eea, #764ba2, #f093fb, #f5576c, #4facfe, #00f2fe) !important;
        background-size: 400% 400% !important;
        animation: gradientShift 15s ease infinite !important;
        position: relative;
        overflow: hidden;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating particles */
    .stApp[data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
        animation: particleFloat 20s ease-in-out infinite;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes particleFloat {
        0%, 100% { transform: translateY(0px) scale(1); }
        50% { transform: translateY(-20px) scale(1.1); }
    }
    
    /* Fun typography */
    .main-title {
        font-family: 'Fredoka One', cursive !important;
        font-size: 3.5rem !important;
        background: linear-gradient(45deg, #4ade80, #60a5fa, #f97316);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: pastelText 4s ease-in-out infinite;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 3px 3px 0px rgba(255, 255, 255, 0.8);
    }
    
    @keyframes pastelText {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        animation: bounceIn 1s ease-out;
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .section-title {
        font-family: 'Fredoka One', cursive;
        font-size: 2.2rem;
        color: white;
        text-align: center;
        margin: 2rem 0 1.5rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        animation: slideInDown 0.8s ease-out;
    }
    
    @keyframes slideInDown {
        from { transform: translateY(-50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Fun card design */
    .fun-card {
        background: var(--card-bg);
        border-radius: var(--border-radius);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px var(--shadow-color);
        border: 3px solid transparent;
        background-clip: padding-box;
        position: relative;
        overflow: hidden;
        animation: cardPop 0.6s ease-out;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes cardPop {
        0% { transform: scale(0.8); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .fun-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #a7f3d0, #93c5fd, #86efac, #bfdbfe, #4ade80);
        animation: pastelBorder 4s linear infinite;
    }
    
    @keyframes pastelBorder {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .fun-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px var(--shadow-color);
        animation: cardBounce 0.6s ease-out;
    }
    
    @keyframes cardBounce {
        0%, 100% { transform: translateY(-10px) scale(1.02); }
        50% { transform: translateY(-15px) scale(1.05); }
    }
    
    /* Fun buttons */
    .stButton > button {
        font-family: 'Fredoka One', cursive !important;
        background: linear-gradient(45deg, #4ade80, #bfdbfe) !important;
        color: rgb(0, 0, 0) !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 1rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 20px rgba(74, 222, 128, 0.3) !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
        animation: buttonPulse 2s ease-in-out infinite !important;
    }
    
    /* Override any dark mode button color */
    .stSidebar .stButton > button {
        color: rgb(0, 0, 0) !important;
    }
    
    /* Override dark mode button color */
    @media (prefers-color-scheme: dark) {
        .stSidebar .stButton > button {
            color: rgb(0, 0, 0) !important;
        }
    }
    
    /* Force black text on all buttons */
    .stButton > button,
    .stButton > button span,
    .stButton > button div,
    .stButton > button p {
        color: rgb(0, 0, 0) !important;
    }
    
    /* Even more specific for sidebar buttons */
    .stSidebar .stButton > button,
    .stSidebar .stButton > button span,
    .stSidebar .stButton > button div,
    .stSidebar .stButton > button p {
        color: rgb(0, 0, 0) !important;
    }
    
    /* Target the actual text content */
    .stButton > button * {
        color: rgb(0, 0, 0) !important;
    }
    
    /* Most specific override */
    .stSidebar .stButton > button * {
        color: rgb(0, 0, 0) !important;
    }
    
    /* Force black text on gratitude journal elements */
    .journal-entry,
    .journal-text,
    .journal-date,
    .journal-time,
    .journal-entry *,
    .journal-text *,
    .journal-date *,
    .journal-time * {
        color: rgb(0, 0, 0) !important;
    }
    
    /* Force black text on badges section elements */
    .badge-card,
    .badge-title,
    .badge-description,
    .badge-requirement,
    .badge-progress,
    .badge-tips,
    .badge-card *,
    .badge-title *,
    .badge-description *,
    .badge-requirement *,
    .badge-progress *,
    .badge-tips * {
        color: rgb(0, 0, 0) !important;
    }
    
    /* Force black text on all div elements in badges section */
    .floating-widget div,
    .widget-card div,
    .floating-widget div *,
    .widget-card div * {
        color: rgb(0, 0, 0) !important;
    }
    
    /* Override any inline styles for badges */
    div[style*="color: #2d5a3d"],
    div[style*="color: #6b7280"],
    div[style*="color: #9ca3af"],
    div[style*="color: #374151"] {
        color: rgb(0, 0, 0) !important;
    }
    
    /* Force black text on all text elements in badges section */
    .floating-widget,
    .widget-card,
    .floating-widget *,
    .widget-card *,
    .floating-widget div,
    .widget-card div,
    .floating-widget div *,
    .widget-card div *,
    .floating-widget p,
    .widget-card p,
    .floating-widget span,
    .widget-card span,
    .floating-widget strong,
    .widget-card strong,
    .floating-widget li,
    .widget-card li {
        color: rgb(0, 0, 0) !important;
    }
    
    /* Force black text on tips list specifically */
    ul[style*="color: rgb(0, 0, 0)"],
    ul[style*="color: #2d5a3d"],
    ul li,
    ul li strong,
    ul li * {
        color: rgb(0, 0, 0) !important;
    }
    
    /* Force black text on tips section specifically */
    div[style*="background: rgba(255,255,255,0.95)"],
    div[style*="background: rgba(255,255,255,0.95)"] *,
    div[style*="border-left: 4px solid #1a5f3c"],
    div[style*="border-left: 4px solid #1a5f3c"] * {
        color: rgb(0, 0, 0) !important;
    }
    
    @keyframes buttonPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.1) !important;
        box-shadow: 0 15px 30px rgba(74, 222, 128, 0.4) !important;
        animation: none !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Fun badges */
    .fun-badge {
        display: inline-flex;
        align-items: center;
        background: linear-gradient(45deg, #ffc800, #ff9600);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 1rem;
        font-weight: 600;
        margin: 0.5rem;
        border: 2px solid white;
        box-shadow: 0 4px 15px rgba(255, 200, 0, 0.3);
        transition: all 0.3s ease;
        animation: badgeSpin 3s ease-in-out infinite;
    }
    
    @keyframes badgeSpin {
        0%, 100% { transform: rotate(0deg) scale(1); }
        25% { transform: rotate(5deg) scale(1.1); }
        75% { transform: rotate(-5deg) scale(1.1); }
    }
    
    .fun-badge:hover {
        transform: rotate(360deg) scale(1.2);
        box-shadow: 0 8px 25px rgba(255, 200, 0, 0.5);
        animation: none;
    }
    
    /* Fun sidebar */
    .stSidebar {
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(10px);
        border-right: 3px solid #58cc02;
    }
    
    /* Dark mode sidebar */
    @media (prefers-color-scheme: dark) {
        .stSidebar {
            background: rgba(30, 41, 59, 0.95) !important;
            border-right: 3px solid #4ade80;
        }
        
        .stSidebar h2, .stSidebar h3, .stSidebar h4 {
            color: #ffffff !important;
        }
        
        .stSidebar p {
            color: #d1d5db !important;
        }
        
        /* Keep button text black for readability */
        .stSidebar .stButton > button {
            color: rgb(0, 0, 0) !important;
        }
        
        /* Keep status section text readable */
        .stSidebar .stMarkdown h4 {
            color: #4ade80 !important;
        }
        
        .stSidebar .stMarkdown p {
            color: #4ade80 !important;
        }
        
        /* Keep badges text readable */
        .stSidebar .badge {
            color: #1f2937 !important;
        }
    }
    
    /* Calming progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #4ade80, #60a5fa) !important;
        border-radius: 10px !important;
        height: 12px !important;
        animation: progressGlow 3s ease-in-out infinite !important;
    }
    
    @keyframes progressGlow {
        0%, 100% { box-shadow: 0 0 8px rgba(74, 222, 128, 0.2); }
        50% { box-shadow: 0 0 15px rgba(96, 165, 250, 0.4); }
    }
    
    /* Dark mode progress bars */
    @media (prefers-color-scheme: dark) {
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #4ade80, #60a5fa, #f97316) !important;
        }
        
        @keyframes progressGlow {
            0%, 100% { box-shadow: 0 0 8px rgba(74, 222, 128, 0.3); }
            50% { box-shadow: 0 0 15px rgba(249, 115, 22, 0.5); }
        }
    }
    
    /* Fun guide character */
    .guide-character {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 80px;
        height: 80px;
        background: linear-gradient(45deg, #4ade80, #bfdbfe);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        color: white;
        box-shadow: 0 8px 25px rgba(74, 222, 128, 0.3);
        cursor: pointer;
        animation: guideBounce 2s ease-in-out infinite;
        z-index: 1000;
    }
    
    @keyframes guideBounce {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .guide-character:hover {
        animation: guideSpin 0.6s ease-out;
    }
    
    @keyframes guideSpin {
        0% { transform: rotate(0deg) scale(1); }
        50% { transform: rotate(180deg) scale(1.2); }
        100% { transform: rotate(360deg) scale(1); }
    }
    
    /* Fun text colors with dark mode support */
    .stMarkdown, .stText, .stWrite, p, div, span, h1, h2, h3, h4, h5, h6 {
        color: var(--text-dark) !important;
    }
    
    /* Dark mode text colors */
    @media (prefers-color-scheme: dark) {
        .stMarkdown, .stText, .stWrite, p, div, span, h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
        }
        
        .main-title {
            text-shadow: 3px 3px 0px rgba(0, 0, 0, 0.8) !important;
        }
        
        .subtitle {
            color: #ffffff !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5) !important;
        }
        
        .section-title {
            color: #ffffff !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5) !important;
        }
        
        .fun-card {
            background: rgba(30, 41, 59, 0.95) !important;
            color: #ffffff !important;
        }
        
        .fun-card h3, .fun-card h4, .fun-card p {
            color: #ffffff !important;
        }
        
        .stButton > button {
            color: #1f2937 !important;
        }
        
        .fun-badge {
            color: #1f2937 !important;
        }
        
        /* Force black text on gratitude journal elements */
        .journal-entry,
        .journal-text,
        .journal-date,
        .journal-time {
            color: rgb(0, 0, 0) !important;
        }
        
        /* Force black text on badges section elements */
        .badge-card,
        .badge-title,
        .badge-description,
        .badge-requirement,
        .badge-progress,
        .badge-tips {
            color: rgb(0, 0, 0) !important;
        }
        
        /* Force black text on all div elements in badges section */
        .floating-widget div,
        .widget-card div,
        .floating-widget div *,
        .widget-card div * {
            color: rgb(0, 0, 0) !important;
        }
        
        /* Override any inline styles for badges */
        div[style*="color: #2d5a3d"],
        div[style*="color: #6b7280"],
        div[style*="color: #9ca3af"],
        div[style*="color: #374151"] {
            color: rgb(0, 0, 0) !important;
        }
        
        /* Force black text on all text elements in badges section */
        .floating-widget,
        .widget-card,
        .floating-widget *,
        .widget-card *,
        .floating-widget div,
        .widget-card div,
        .floating-widget div *,
        .widget-card div *,
        .floating-widget p,
        .widget-card p,
        .floating-widget span,
        .widget-card span,
        .floating-widget strong,
        .widget-card strong,
        .floating-widget li,
        .widget-card li {
            color: rgb(0, 0, 0) !important;
        }
        
        /* Force black text on tips list specifically */
        ul[style*="color: rgb(0, 0, 0)"],
        ul[style*="color: #2d5a3d"],
        ul li,
        ul li strong,
        ul li * {
            color: rgb(0, 0, 0) !important;
        }
        
        /* Force black text on tips section specifically */
        div[style*="background: rgba(255,255,255,0.95)"],
        div[style*="background: rgba(255,255,255,0.95)"] *,
        div[style*="border-left: 4px solid #1a5f3c"],
        div[style*="border-left: 4px solid #1a5f3c"] * {
            color: rgb(0, 0, 0) !important;
        }
    }
    
    /* Fun input styling */
    .stTextInput > div > div > input {
        border-radius: 15px !important;
        border: 2px solid #58cc02 !important;
        transition: all 0.3s ease !important;
        background: white !important;
        color: var(--text-dark) !important;
        animation: inputGlow 3s ease-in-out infinite !important;
    }
    
    /* Dark mode input styling */
    @media (prefers-color-scheme: dark) {
        .stTextInput > div > div > input {
            background: #374151 !important;
            color: #ffffff !important;
            border-color: #4ade80 !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #9ca3af !important;
        }
    }
    
    @keyframes inputGlow {
        0%, 100% { box-shadow: 0 0 5px rgba(88, 204, 2, 0.2); }
        50% { box-shadow: 0 0 15px rgba(88, 204, 2, 0.4); }
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ffc800 !important;
        box-shadow: 0 0 20px rgba(255, 200, 0, 0.4) !important;
        animation: none !important;
    }
    
    /* Fun slider */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #58cc02, #ffc800) !important;
    }
    
    /* Fun alerts */
    .stAlert {
        border-radius: 15px !important;
        border: 2px solid #58cc02 !important;
        box-shadow: 0 8px 20px rgba(88, 204, 2, 0.2) !important;
    }
    
    /* Fun charts */
    .js-plotly-plot {
        background: transparent !important;
    }
    
    /* Container adjustments */
    .block-container {
        padding: 2rem;
        max-width: 1200px;
    }
    
    /* Fun dividers */
    .stDivider {
        border-top: 3px solid #58cc02 !important;
        margin: 2rem 0 !important;
        position: relative;
    }
    
    .stDivider::after {
        content: '🌟';
        position: absolute;
        top: -15px;
        left: 50%;
        transform: translateX(-50%);
        background: white;
        padding: 0 10px;
        font-size: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

if 'points' not in st.session_state:
    st.session_state.points = 0
if 'moods' not in st.session_state:
    st.session_state.moods = []
if 'screen_times' not in st.session_state:
    st.session_state.screen_times = []
if 'gratitudes' not in st.session_state:
    st.session_state.gratitudes = []
if 'pomodoro_completed' not in st.session_state:
    st.session_state.pomodoro_completed = 0
if 'breathing_completed' not in st.session_state:
    st.session_state.breathing_completed = 0
if 'badge_celebration' not in st.session_state:
    st.session_state.badge_celebration = None
if 'previous_badges' not in st.session_state:
    st.session_state.previous_badges = []

if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False
if 'timer_seconds' not in st.session_state:
    st.session_state.timer_seconds = 0
if 'timer_mode' not in st.session_state:
    st.session_state.timer_mode = 'focus'
if 'last_timer_update' not in st.session_state:
    st.session_state.last_timer_update = time.time()

if 'music_playing' not in st.session_state:
    st.session_state.music_playing = False
if 'current_track' not in st.session_state:
    st.session_state.current_track = "None"
if 'volume' not in st.session_state:
    st.session_state.volume = 0.5

if 'open_chatbot' in st.query_params:
    st.session_state.current_section = "chatbot"
    st.query_params.clear()

def get_level_and_badges(points):
    """Determine user level and badges based on points"""
    levels = {
        0: "Beginner",
        50: "Mindful Explorer", 
        100: "Zen Master",
        200: "Wellness Warrior",
        300: "Mindfulness Guru"
    }
    
    badges = []
    badge_emojis = {}
    
    if points >= 10:
        badges.append("🌟 First Steps")
        badge_emojis["🌟 First Steps"] = "🌟"
    if points >= 50:
        badges.append("🎯 Goal Setter")
        badge_emojis["🎯 Goal Setter"] = "🎯"
    if points >= 100:
        badges.append("🧘‍♀️ Zen Master")
        badge_emojis["🧘‍♀️ Zen Master"] = "🧘‍♀️"
    if points >= 200:
        badges.append("💎 Wellness Warrior")
        badge_emojis["💎 Wellness Warrior"] = "💎"
    if points >= 300:
        badges.append("👑 Mindfulness Guru")
        badge_emojis["👑 Mindfulness Guru"] = "👑"
    
    current_level = "Beginner"
    for threshold, level in levels.items():
        if points >= threshold:
            current_level = level
    
    return current_level, badges, badge_emojis

def check_for_new_badges(points):
    """Check if user earned new badges and trigger celebration"""
    current_level, current_badges, badge_emojis = get_level_and_badges(points)
    
    new_badges = []
    for badge in current_badges:
        if badge not in st.session_state.previous_badges:
            new_badges.append(badge)
    
    st.session_state.previous_badges = current_badges.copy()
    
    for badge in new_badges:
        if badge in badge_emojis:
            st.session_state.badge_celebration = {
                'name': badge,
                'emoji': badge_emojis[badge]
            }
            st.session_state.current_section = "home"
            st.success(f"🎉 NEW BADGE EARNED: {badge}!")
    
    return new_badges

DAILY_TIPS = [
    "📱 Take a 20-minute screen break every 2 hours to reduce eye strain",
    "🌙 Avoid screens 1 hour before bedtime for better sleep quality",
    "🚶‍♀️ Replace 30 minutes of screen time with physical activity",
    "👥 Have face-to-face conversations instead of texting when possible",
    "🌿 Spend time in nature to balance digital exposure",
    "📚 Read a physical book instead of digital content for 15 minutes",
    "🎨 Try a creative activity like drawing or writing without screens",
    "🧘‍♀️ Practice mindfulness for 5 minutes when feeling overwhelmed by screens"
]

BREAK_ACTIVITIES = [
    "🧘‍♀️ Do a quick 5-minute meditation",
    "💪 Take a short walk around your room",
    "🎵 Listen to calming music with your eyes closed",
    "📖 Read a few pages of a physical book",
    "🎨 Doodle or sketch something creative",
    "💭 Practice deep breathing exercises",
    "🏃‍♀️ Do some light stretching or yoga poses",
    "🌱 Water your plants or look out the window",
    "✍️ Write down three things you're grateful for",
    "🎯 Organize your study space for 5 minutes"
]

OPENAI_API_KEY = "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"

def show_how_to_use_section():
    """How to Use section with comprehensive guide"""
    st.markdown('<h1 class="section-title">📚 How to Use MindfulStudy Hub</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="fun-card">
        <h3 style="color: #58cc02; margin-bottom: 20px; font-family: 'Fredoka One', cursive; font-size: 1.8rem;">🚀 Welcome to Your Wellness Journey!</h3>
        <p style="font-size: 1.1rem; line-height: 1.6; color: #2d3748; margin-bottom: 25px;">
            MindfulStudy Hub is your comprehensive wellness companion designed to help you maintain balance between digital life and mental well-being. 
            Here's everything you need to know to get started!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="fun-card">
            <h4 style="color: #4ade80; margin-bottom: 15px; font-family: 'Fredoka One', cursive;">🌟 Calm Points System</h4>
            <p style="color: #4a5568; line-height: 1.5;">
                <strong>How it works:</strong> Complete activities to earn points and level up!<br><br>
                <strong>Points earned for:</strong><br>
                • Logging mood: 5 points<br>
                • Tracking screen time: 5 points<br>
                • Writing gratitude: 10 points<br>
                • Breathing exercises: 10 points<br>
                • Pomodoro sessions: 20 points<br>
                • Random activities: 5 points
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="fun-card">
            <h4 style="color: #60a5fa; margin-bottom: 15px; font-family: 'Fredoka One', cursive;">📊 Daily Tracking</h4>
            <p style="color: #4a5568; line-height: 1.5;">
                <strong>Mood Tracker:</strong> Rate your mood from 1-10 daily to track emotional patterns.<br><br>
                <strong>Screen Time Tracker:</strong> Log your daily screen usage to maintain digital balance.<br><br>
                <strong>Benefits:</strong> Identify patterns and make informed wellness decisions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="fun-card">
            <h4 style="color: #f97316; margin-bottom: 15px; font-family: 'Fredoka One', cursive;">🫁 Breathing Exercise</h4>
            <p style="color: #4a5568; line-height: 1.5;">
                <strong>What it does:</strong> Guided 3-breath mindfulness exercise with animated visuals.<br><br>
                <strong>How to use:</strong> Click "Start Breathing Exercise" and follow the animated circles.<br><br>
                <strong>Benefits:</strong> Reduces stress, improves focus, and promotes calmness.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="fun-card">
            <h4 style="color: #4ade80; margin-bottom: 15px; font-family: 'Fredoka One', cursive;">⏰ Pomodoro Timer</h4>
            <p style="color: #4a5568; line-height: 1.5;">
                <strong>Focus Session:</strong> 25-minute focused work periods.<br><br>
                <strong>Break Session:</strong> 5-minute restorative breaks.<br><br>
                <strong>How to use:</strong> Choose "Start Focus" or "Start Break" and let the timer guide you.<br><br>
                <strong>Benefits:</strong> Improves productivity and prevents burnout.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="fun-card">
            <h4 style="color: #60a5fa; margin-bottom: 15px; font-family: 'Fredoka One', cursive;">📝 Gratitude Journal</h4>
            <p style="color: #4a5568; line-height: 1.5;">
                <strong>What it is:</strong> Interactive digital journal with book-like interface.<br><br>
                <strong>How to use:</strong> Write what you're grateful for and navigate through your entries.<br><br>
                <strong>Benefits:</strong> Cultivates positive mindset and emotional well-being.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="fun-card">
            <h4 style="color: #f97316; margin-bottom: 15px; font-family: 'Fredoka One', cursive;">💬 AI Therapist</h4>
            <p style="color: #4a5568; line-height: 1.5;">
                <strong>What it is:</strong> Supportive AI companion for mental health conversations.<br><br>
                <strong>How to use:</strong> Chat naturally about your feelings and receive empathetic responses.<br><br>
                <strong>Benefits:</strong> Provides emotional support and coping strategies.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 💡 Tips for Best Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("**🎯 Consistency is Key**")
            st.write("Log your mood and screen time daily to build healthy habits and track your progress over time.")
            
            st.markdown("**⏰ Use the Timer Regularly**")
            st.write("Incorporate Pomodoro sessions into your study routine to maintain focus and prevent mental fatigue.")
            
            st.markdown("**🫁 Practice Mindfulness**")
            st.write("Use breathing exercises when feeling stressed or overwhelmed to regain mental clarity.")
    
    with col2:
        with st.container():
            st.markdown("**📝 Reflect Daily**")
            st.write("Write in your gratitude journal regularly to cultivate a positive mindset and emotional resilience.")
            
            st.markdown("**🏆 Celebrate Progress**")
            st.write("Earn badges and track your wellness journey to stay motivated and recognize your achievements.")
            
            st.markdown("**💬 Seek Support**")
            st.write("Use the AI Therapist when you need someone to talk to or want to explore your feelings.")
    
    st.markdown("### 🧭 Navigation Guide")
    st.write("Use the sidebar navigation to explore different features. Each section is designed to support a specific aspect of your wellness journey:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🏠 Home & Progress**")
        st.write("View your points, badges, and daily tips")
        
        st.markdown("**📊 Daily Tracking**")
        st.write("Log your mood and screen time")
        
        st.markdown("**📝 Gratitude Journal**")
        st.write("Write and review gratitude entries")
    
    with col2:
        st.markdown("**🫁 Breathing Exercise**")
        st.write("Guided mindfulness practice")
        
        st.markdown("**⏰ Pomodoro Timer**")
        st.write("Focus and break sessions")
        
        st.markdown("**📈 Progress Dashboard**")
        st.write("View charts and statistics")
    
    with col3:
        st.markdown("**🎯 Activity Suggestions**")
        st.write("Break activity recommendations")
        
        st.markdown("**🏆 Badges Collection**")
        st.write("View earned and available badges")
        
        st.markdown("**💬 AI Therapist**")
        st.write("Mental health support chat")

def main():
    if 'loading_complete' not in st.session_state:
        st.session_state.loading_complete = False
    
    if not st.session_state.loading_complete:
        st.markdown("""
        <div id="loading-screen" style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            animation: fadeIn 1s ease-in;
        ">
            <div style="
                text-align: center;
                color: white;
                font-family: 'Inter', sans-serif;
            ">
                <div style="
                    font-size: 3rem;
                    margin-bottom: 1rem;
                    animation: pulse 2s ease-in-out infinite;
                ">🧘‍♀️</div>
                <div style="
                    font-size: 2.5rem;
                    font-weight: 600;
                    margin-bottom: 1rem;
                    animation: slideInUp 1s ease-out 0.5s both;
                ">MindfulStudy Hub</div>
                <div style="
                    font-size: 1.2rem;
                    opacity: 0.9;
                    margin-bottom: 2rem;
                    animation: slideInUp 1s ease-out 1s both;
                ">Your journey to wellness begins here</div>
                <div style="
                    width: 200px;
                    height: 4px;
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 2px;
                    overflow: hidden;
                    animation: slideInUp 1s ease-out 1.5s both;
                    margin: 0 auto;
                ">
                    <div style="
                        width: 100%;
                        height: 100%;
                        background: linear-gradient(90deg, #fff, #f0f0f0);
                        border-radius: 2px;
                        animation: loadingBar 3s ease-in-out infinite;
                        transform-origin: left center;
                    "></div>
                </div>
                <div style="
                    margin-top: 1rem;
                    font-size: 0.9rem;
                    opacity: 0.7;
                    animation: slideInUp 1s ease-out 2s both;
                ">Loading your wellness experience...</div>
            </div>
        </div>
        
        <style>
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        
        @keyframes loadingBar {
            0% { transform: translateX(-100%); }
            50% { transform: translateX(0%); }
            100% { transform: translateX(100%); }
        }
        </style>
        
        <script>
        // Auto-hide loading screen after 4 seconds
        setTimeout(function() {
            document.getElementById('loading-screen').style.animation = 'fadeOut 1s ease-out forwards';
            setTimeout(function() {
                document.getElementById('loading-screen').style.display = 'none';
            }, 1000);
        }, 4000);
        
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
        </script>
        """, unsafe_allow_html=True)
        
        time.sleep(4)
        st.session_state.loading_complete = True
        st.rerun()
    

    
    st.markdown("""
    <div class="guide-character" onclick="openAIChat()">
        🧘‍♀️
    </div>
    
    <script>
    function openAIChat() {
        // Trigger the AI Therapist button in the sidebar
        const buttons = document.querySelectorAll('button');
        for (let button of buttons) {
            if (button.textContent.includes('AI Therapist')) {
                button.click();
                break;
            }
        }
    }
    
    console.log('AI Chat button loaded');
    </script>
    """, unsafe_allow_html=True)
    
    if st.session_state.badge_celebration:
        celebration = st.session_state.badge_celebration
        st.markdown(f"""
        <script>
        console.log('Triggering badge celebration for: {celebration['name']}');
        triggerBadgeCelebration('{celebration['name']}', '{celebration['emoji']}');
        </script>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: linear-gradient(135deg, #4ade80 0%, #60a5fa 50%, #f97316 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(74, 222, 128, 0.3);
            z-index: 10000;
            text-align: center;
            animation: slideDown 0.5s ease-out;
            border: 2px solid rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(10px);
            min-width: 300px;
        ">
            <div style="font-size: 2rem; margin-bottom: 10px;">{celebration['emoji']}</div>
            <div style="font-size: 1.5rem; font-weight: bold; margin-bottom: 5px;">🎉 BADGE EARNED! 🎉</div>
            <div style="font-size: 1.2rem;">{celebration['name']}</div>
        </div>
        
        <style>
        @keyframes slideDown {{
            0% {{ transform: translateX(-50%) translateY(-100px); opacity: 0; }}
            100% {{ transform: translateX(-50%) translateY(0); opacity: 1; }}
        }}
        </style>
        """, unsafe_allow_html=True)
        
        st.balloons()
        st.session_state.badge_celebration = None
    
    with st.sidebar:
        current_level, badges, _ = get_level_and_badges(st.session_state.points)
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #4ade80 0%, #60a5fa 50%, #f97316 100%);
            color: white;
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(74,222,128,0.3);
        ">
            <div style="font-size: 1.2rem; font-weight: bold; margin-bottom: 5px;">Current Level</div>
            <div style="font-size: 2rem; font-weight: bold;">{current_level}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h2 style="color: #1a5f3c; margin-bottom: 30px;">🧘‍♀️ Navigation</h2>
        </div>
        """, unsafe_allow_html=True)
        

        
        if st.button("📚 How to Use", use_container_width=True, disabled=st.session_state.timer_running):
            st.session_state.current_section = "how_to_use"
            st.rerun()
        if st.button("🏠 Home & Progress", use_container_width=True, disabled=st.session_state.timer_running):
            st.session_state.current_section = "home"
            st.rerun()
        if st.button("📊 Daily Tracking", use_container_width=True, disabled=st.session_state.timer_running):
            st.session_state.current_section = "tracking"
            st.rerun()
        if st.button("📝 Gratitude Journal", use_container_width=True, disabled=st.session_state.timer_running):
            st.session_state.current_section = "gratitude"
            st.rerun()
        if st.button("🫁 Breathing Exercise", use_container_width=True, disabled=st.session_state.timer_running):
            st.session_state.current_section = "breathing"
            st.rerun()
        if st.button("⏰ Pomodoro Timer", use_container_width=True, disabled=st.session_state.timer_running):
            st.session_state.current_section = "pomodoro"
            st.rerun()
        if st.button("📈 Progress Dashboard", use_container_width=True, disabled=st.session_state.timer_running):
            st.session_state.current_section = "dashboard"
            st.rerun()
        if st.button("🎯 Activity Suggestions", use_container_width=True, disabled=st.session_state.timer_running):
            st.session_state.current_section = "activities"
            st.rerun()
        if st.button("🏆 Badges Collection", use_container_width=True, disabled=st.session_state.timer_running):
            st.session_state.current_section = "badges"
            st.rerun()
        if st.button("💬 AI Therapist", use_container_width=True, disabled=st.session_state.timer_running):
            st.session_state.current_section = "chatbot"
            st.rerun()
        st.markdown("---")
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 20px; margin: 20px 0;">
            <h4 style="color: #4ade80; text-align: center;">🌟 Current Status</h4>
            <p style="text-align: center; font-size: 1.5rem; font-weight: bold; color: #4ade80;">{st.session_state.points} Points</p>
            <div style="margin-top: 15px; text-align: center;">
                <p style="color: #60a5fa; font-size: 0.9rem; margin-bottom: 8px;">🏆 Badges Earned:</p>
                <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 5px;">
                    {''.join([f'<div class="badge" style="font-size: 0.9rem; padding: 4px 8px;">{badge}</div>' for badge in badges]) if badges else '<span style="color: #6b7280; font-style: italic; font-size: 0.8rem;">No badges yet</span>'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if 'current_section' not in st.session_state:
        st.session_state.current_section = "home"
    
    current_level, badges, _ = get_level_and_badges(st.session_state.points)
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        pass
    
    with col2:
        st.markdown(f"""
        <div style="position: fixed; top: 20px; right: 20px; z-index: 1000; background: linear-gradient(135deg, #4ade80 0%, #60a5fa 50%, #f97316 100%); 
                    color: white; padding: 15px; border-radius: 25px; box-shadow: 0 4px 15px rgba(74,222,128,0.3); 
                    text-align: center; min-width: 120px;">
            <div style="font-size: 0.9rem; margin-bottom: 5px;">🌟 Calm Points</div>
            <div style="font-size: 1.8rem; font-weight: bold; background: linear-gradient(45deg, #ff0000, #ff8000, #ffff00, #80ff00, #00ff00, #00ff80, #00ffff, #0080ff, #0000ff, #8000ff, #ff00ff, #ff0080); background-size: 300% 300%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: rainbowShift 3s ease-in-out infinite;">{st.session_state.points}</div>
            <div style="font-size: 0.8rem; margin-top: 5px;">{current_level}</div>
        </div>
        
        <style>
        @keyframes rainbowShift {{
            0%, 100% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
        }}
        </style>
        """, unsafe_allow_html=True)
    
    with col3:
        pass
    
    if st.session_state.current_section == "home":
        show_home_section()
    elif st.session_state.current_section == "tracking":
        show_tracking_section()
    elif st.session_state.current_section == "gratitude":
        show_gratitude_section()
    elif st.session_state.current_section == "breathing":
        show_breathing_section()
    elif st.session_state.current_section == "pomodoro":
        show_pomodoro_section()
    elif st.session_state.current_section == "dashboard":
        show_dashboard_section()
    elif st.session_state.current_section == "activities":
        show_activities_section()
    elif st.session_state.current_section == "badges":
        show_badges_section()
    elif st.session_state.current_section == "chatbot":
        show_chatbot_section()
    elif st.session_state.current_section == "how_to_use":
        show_how_to_use_section()

def show_home_section():
    """Home section with fun Duolingo-style design"""
    
    st.markdown('<h1 class="main-title">🧘‍♀️ MindfulStudy Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your Wellness Adventure - Learn & Grow! 🚀</p>', unsafe_allow_html=True)
    
    current_level, badges, _ = get_level_and_badges(st.session_state.points)
    
    if badges:
        badge_info = {
            "🌟 First Steps": {
                "emoji": "🌟",
                "description": "You've taken your first steps on your wellness journey! This badge celebrates your commitment to personal growth and mindfulness.",
                "requirement": "Earn 10 points"
            },
            "🎯 Goal Setter": {
                "emoji": "🎯",
                "description": "You've shown dedication to setting and achieving wellness goals. Your consistent effort is building healthy habits!",
                "requirement": "Earn 50 points"
            },
            "🧘‍♀️ Zen Master": {
                "emoji": "🧘‍♀️",
                "description": "You've achieved a balanced state of mind through regular mindfulness practices. Your inner peace is growing!",
                "requirement": "Earn 100 points"
            },
            "💎 Wellness Warrior": {
                "emoji": "💎",
                "description": "You've demonstrated exceptional dedication to wellness. Your commitment to self-care is truly inspiring!",
                "requirement": "Earn 200 points"
            },
            "👑 Mindfulness Guru": {
                "emoji": "👑",
                "description": "You've reached the pinnacle of mindful living. Your wisdom and dedication make you a true wellness champion!",
                "requirement": "Earn 300 points"
            }
        }
        

        
        st.markdown(f"""
        <div class="fun-card" style="text-align: center;">
            <h3 style="color: #58cc02; margin-bottom: 15px; font-family: 'Fredoka One', cursive; font-size: 1.5rem;">🏆 Your Awesome Badges!</h3>
            <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 10px;">
                {''.join([f'<div class="fun-badge">{badge}</div>' for badge in badges])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="fun-card" style="text-align: center;">
            <h3 style="color: #58cc02; margin-bottom: 15px; font-family: 'Fredoka One', cursive; font-size: 1.5rem;">🏆 Your Badges</h3>
            <div style="
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 80px;
                color: #4a5568;
            ">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 15px; animation: sparkle 2s ease-in-out infinite;">🌟</div>
                    <div style="font-weight: 600; font-size: 1.2rem; margin-bottom: 10px;">No badges yet!</div>
                    <div style="font-size: 1rem; color: #718096;">Start your wellness journey to earn your first badge! 🚀</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div class="fun-card" style="text-align: center;">
            <h3 style="font-size: 1.2rem; color: #58cc02; margin-bottom: 10px; font-family: 'Fredoka One', cursive;">🌟 Calm Points</h3>
            <h2 style="font-size: 3rem; margin: 0; font-weight: 700; background: linear-gradient(45deg, #ff0000, #ff8000, #ffff00, #80ff00, #00ff00, #00ff80, #00ffff, #0080ff, #0000ff, #8000ff, #ff00ff, #ff0080); background-size: 300% 300%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; animation: rainbowShift 3s ease-in-out infinite;">{st.session_state.points}</h2>
            <p style="color: #4a5568; margin-top: 5px; font-size: 1rem;">Keep earning points! 💪</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        next_level_points = 50 if st.session_state.points < 50 else (100 if st.session_state.points < 100 else 200)
        if st.session_state.points < 300:
            progress_percent = st.session_state.points / next_level_points
            st.markdown(f"""
            <div class="fun-card">
                <h4 style="color: #58cc02; margin-bottom: 15px; font-family: 'Fredoka One', cursive; font-size: 1.3rem;">📈 Level Progress</h4>
                <div style="background: #e2e8f0; border-radius: 15px; height: 15px; margin: 15px 0; overflow: hidden; border: 2px solid #4ade80;">
                    <div style="background: linear-gradient(90deg, #4ade80, #60a5fa); width: {progress_percent*100}%; height: 100%; border-radius: 15px; transition: width 0.6s ease; animation: progressPulse 3s ease-in-out infinite;"></div>
                </div>
                <p style="color: #4a5568; font-size: 1rem; margin: 0; text-align: center;">{next_level_points - st.session_state.points} points to next level! 🎯</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="stDivider"></div>', unsafe_allow_html=True)
    
    tip = random.choice(DAILY_TIPS)
    st.markdown(f"""
    <div class="fun-card">
        <h3 style="color: #58cc02; margin-bottom: 15px; font-family: 'Fredoka One', cursive; font-size: 1.5rem;">💡 Today's Wellness Tip</h3>
        <p style="font-size: 1.2rem; margin: 0; color: #2d3748; line-height: 1.6; text-align: center;">{tip}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    @keyframes numberBounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    @keyframes progressPulse {
        0%, 100% { box-shadow: 0 0 8px rgba(74, 222, 128, 0.2); }
        50% { box-shadow: 0 0 15px rgba(96, 165, 250, 0.4); }
    }
    
    @keyframes sparkle {
        0%, 100% { transform: scale(1) rotate(0deg); }
        50% { transform: scale(1.3) rotate(180deg); }
    }
    
    @keyframes rainbowShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    </style>
    """, unsafe_allow_html=True)

def show_tracking_section():
    """Daily tracking section"""
    st.markdown('<h1 class="section-title">📊 Daily Tracking</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="widget-card">', unsafe_allow_html=True)
        st.write("**📱 Screen Time Tracker**")
        screen_time = st.slider("Hours of screen time today", 0, 12, 4, key="screen_slider")
        
        if st.button("🎯 Log Screen Time", key="screen_btn", use_container_width=True):
            st.session_state.screen_times.append(screen_time)
            st.session_state.points += 5
            
            if screen_time > 4:
                st.warning("⚠️ Consider reducing screen time for better mental health!")
            elif screen_time < 5:
                st.success("🎉 Great job keeping screen time balanced!")
                st.session_state.points += 5
            
            check_for_new_badges(st.session_state.points)
            
            st.balloons()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="widget-card">', unsafe_allow_html=True)
        st.write("**😊 Mood Tracker**")
        mood = st.slider("How are you feeling today? (1-10)", 1, 10, 5, key="mood_slider")
        
        if st.button("💭 Log Mood", key="mood_btn", use_container_width=True):
            st.session_state.moods.append(mood)
            st.session_state.points += 5
            
            if mood >= 7:
                st.success("😊 Wonderful! Keep up the positive energy!")
            elif mood <= 3:
                st.info("🤗 Remember, it's okay to not be okay. Consider trying the breathing exercise.")
            
            check_for_new_badges(st.session_state.points)
            
            st.balloons()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

def show_gratitude_section():
    """Gratitude journal section"""
    st.markdown('<h1 class="section-title">📝 Gratitude Journal</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="widget-card">', unsafe_allow_html=True)
    st.write("**Write down something you're grateful for today:**")
    
    gratitude_entry = st.text_area("What are you thankful for?", key="gratitude_text", height=100)
    
    if st.button("🙏 Add Gratitude Entry", key="gratitude_btn", use_container_width=True):
        if gratitude_entry.strip():
            st.session_state.gratitudes.append({
                'entry': gratitude_entry,
                'date': datetime.now().strftime("%A, %B %d, %Y"),
                'time': datetime.now().strftime("%I:%M %p")
            })
            st.session_state.points += 10
            st.success("🙏 Thank you for sharing your gratitude!")
            
            check_for_new_badges(st.session_state.points)
            
            st.balloons()
            st.rerun()
        else:
            st.error("Please write something before submitting.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.gratitudes:
        st.markdown('<div class="floating-widget">', unsafe_allow_html=True)
        st.write("**🌟 Your Gratitude Journey:**")
        if len(st.session_state.gratitudes) > 0:
            if 'journal_page' not in st.session_state:
                st.session_state.journal_page = 0
            
            if st.session_state.get('page_changed', False):
                st.session_state.page_changed = False
            
            entries_per_page = 1
            total_pages = max(1, len(st.session_state.gratitudes))
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("◀ Previous", disabled=st.session_state.journal_page == 0, use_container_width=True):
                    st.session_state.journal_page = max(0, st.session_state.journal_page - 1)
                    st.session_state.page_changed = True
                    st.rerun()
            
            with col2:
                st.markdown(f"""
                <div style="text-align: center; padding: 10px; background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%); 
                            border-radius: 15px; border: 2px solid #c3e6cb; color: #2d5a3d; font-weight: bold;">
                    📖 Page {st.session_state.journal_page + 1} of {total_pages}
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                if st.button("Next ▶", disabled=st.session_state.journal_page >= total_pages - 1, use_container_width=True):
                    st.session_state.journal_page = min(total_pages - 1, st.session_state.journal_page + 1)
                    st.session_state.page_changed = True
                    st.rerun()
            
            st.markdown("""
            <style>
            @keyframes pageFlip {
                0% { transform: rotateY(0deg) scale(1); opacity: 1; }
                50% { transform: rotateY(-15deg) scale(0.95); opacity: 0.7; }
                100% { transform: rotateY(0deg) scale(1); opacity: 1; }
            }
            
            .journal-book {
                perspective: 1200px;
                margin: 30px 0;
                display: flex;
                justify-content: center;
            }
            
            .journal-page {
                background: linear-gradient(135deg, #fefefe 0%, #f8f9fa 50%, #f1f3f4 100%);
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 40px 50px;
                margin: 20px 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05), 0 10px 15px rgba(0,0,0,0.1), 0 20px 25px rgba(0,0,0,0.15);
                transform-style: preserve-3d;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                min-height: 300px;
                max-width: 600px;
                width: 100%;
                background-image: linear-gradient(90deg, transparent 0%, transparent 49%, #e5e7eb 49%, #e5e7eb 51%, transparent 51%, transparent 100%), linear-gradient(135deg, #fefefe 0%, #f8f9fa 50%, #f1f3f4 100%);
                background-size: 100% 100%, 100% 100%;
            }
            
            .journal-page.animate {
                animation: pageFlip 0.8s ease-out;
            }
            
            .journal-page::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, #d1d5db, transparent);
            }
            
            .journal-page::after {
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, #d1d5db, transparent);
            }
            
            .journal-page:hover {
                transform: translateY(-3px) rotateY(2deg);
                box-shadow: 0 6px 8px rgba(0,0,0,0.08), 0 15px 20px rgba(0,0,0,0.12), 0 25px 30px rgba(0,0,0,0.18);
            }
            
            .journal-entry {
                background: transparent;
                padding: 0;
                margin: 0;
                border: none;
                box-shadow: none;
                color: rgb(0, 0, 0) !important;
                font-family: 'Georgia', 'Times New Roman', serif;
                line-height: 1.8;
                position: relative;
                overflow: visible;
            }
            
            .journal-date {
                font-weight: 600;
                color: rgb(0, 0, 0) !important;
                font-size: 1.1em;
                margin-bottom: 10px;
                text-transform: none;
                letter-spacing: 0.5px;
                font-family: 'Caveat', 'Dancing Script', 'Segoe Script', cursive;
            }
            
            .journal-time {
                font-weight: 400;
                color: rgb(0, 0, 0) !important;
                font-size: 0.9em;
                margin-bottom: 25px;
                text-transform: none;
                letter-spacing: 0.5px;
                border-bottom: 2px solid #e5e7eb;
                padding-bottom: 15px;
                font-family: 'Caveat', 'Dancing Script', 'Segoe Script', cursive;
            }
            
            .journal-text {
                font-style: normal;
                font-size: 1.3em;
                color: rgb(0, 0, 0) !important;
                text-align: justify;
                line-height: 1.9;
                margin-top: 20px;
                padding: 20px 0;
                border-left: 3px solid #1a5f3c;
                padding-left: 25px;
                background: linear-gradient(135deg, rgba(26,95,60,0.03) 0%, rgba(45,90,61,0.02) 100%);
                border-radius: 0 8px 8px 0;
                word-wrap: break-word;
                overflow-wrap: break-word;
                hyphens: auto;
                max-height: 200px;
                overflow-y: auto;
                font-family: 'Caveat', 'Dancing Script', 'Segoe Script', cursive;
            }
            
            .page-number {
                position: absolute;
                bottom: 20px;
                right: 30px;
                font-size: 0.9em;
                color: #9ca3af;
                font-style: italic;
                font-family: 'Caveat', 'Dancing Script', 'Segoe Script', cursive;
            }
            
            .page-header {
                position: absolute;
                top: 20px;
                left: 30px;
                font-size: 0.8em;
                color: #9ca3af;
                font-family: 'Caveat', 'Dancing Script', 'Segoe Script', cursive;
            }
            
            /* Force black text on gratitude journal in dark mode */
            @media (prefers-color-scheme: dark) {
                .journal-entry,
                .journal-text,
                .journal-date,
                .journal-time {
                    color: rgb(0, 0, 0) !important;
                }
            }
            </style>
            """, unsafe_allow_html=True)
            
            start_idx = st.session_state.journal_page * entries_per_page
            end_idx = min(start_idx + entries_per_page, len(st.session_state.gratitudes))
            page_entries = list(reversed(st.session_state.gratitudes))[start_idx:end_idx]
            
            if st.session_state.get('page_changed', False):
                with st.spinner("📖 Flipping page..."):
                    time.sleep(0.3)  # Brief pause for animation effect
            
            st.markdown('<div class="journal-book">', unsafe_allow_html=True)
            
            for i, entry in enumerate(page_entries):
                animation_class = "animate" if st.session_state.get('page_changed', False) else ""
                st.markdown(f"""
                <div class="journal-page {animation_class}">
                    <div class="page-header">Gratitude Journal</div>
                    <div class="journal-entry">
                        <div class="journal-date">📅 {entry['date']}</div>
                        <div class="journal-time">🕐 {entry.get('time', 'Time not recorded')}</div>
                        <div class="journal-text">"{entry['entry']}"</div>
                    </div>
                    <div class="page-number">Page {st.session_state.journal_page + 1} of {total_pages}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if len(page_entries) == 0:
                st.markdown("""
                <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%); 
                            border-radius: 20px; border: 2px dashed #c3e6cb; color: #2d5a3d;">
                    <h3>📖 Your Gratitude Journal</h3>
                    <p>Start your journey by writing your first gratitude entry above!</p>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_breathing_section():
    """Breathing exercise section"""
    st.markdown('<h1 class="section-title">🫁 Breathing Exercise</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="widget-card">', unsafe_allow_html=True)
    st.write("**Take a moment to reset with this 3-breath guided exercise:**")
    
    if st.button("🫁 Start Breathing Exercise", key="breathing_btn", use_container_width=True):
        st.session_state.breathing_completed += 1
        
        breath_placeholder = st.empty()
        
        st.markdown("""
        <style>
        .breathing-container {
            position: relative;
            width: 500px;
            height: 500px;
            margin: 2rem auto;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .breathing-circle {
            position: absolute;
            border-radius: 50%;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation: breathe 10s ease-in-out infinite;
        }
        
        .circle-1 {
            width: 100px;
            height: 100px;
            background: radial-gradient(circle, #4ade80, #22c55e);
            animation-delay: 0s;
        }
        
        .circle-2 {
            width: 150px;
            height: 150px;
            background: radial-gradient(circle, #60a5fa, #3b82f6);
            animation-delay: 0.2s;
        }
        
        .circle-3 {
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, #f97316, #ea580c);
            animation-delay: 0.4s;
        }
        
        .circle-4 {
            width: 250px;
            height: 250px;
            background: radial-gradient(circle, #4ade80, #22c55e);
            animation-delay: 0.6s;
        }
        
        .circle-5 {
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, #60a5fa, #3b82f6);
            animation-delay: 0.8s;
        }
        
        .circle-6 {
            width: 350px;
            height: 350px;
            background: radial-gradient(circle, #f97316, #ea580c);
            animation-delay: 1s;
        }
        
        @keyframes breathe {
            0%, 100% {
                transform: translate(-50%, -50%) scale(0.3);
                opacity: 0.3;
            }
            25% {
                transform: translate(-50%, -50%) scale(0.6);
                opacity: 0.6;
            }
            50% {
                transform: translate(-50%, -50%) scale(1);
                opacity: 0.8;
            }
            75% {
                transform: translate(-50%, -50%) scale(0.6);
                opacity: 0.6;
            }
        }
        
        .breathing-text {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            font-family: 'Fredoka One', cursive;
            font-size: 1.5rem;
            color: white;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
            z-index: 10;
            text-align: center;
            background: rgba(0, 0, 0, 0.3);
            padding: 10px 20px;
            border-radius: 15px;
            backdrop-filter: blur(5px);
        }
        </style>
        """, unsafe_allow_html=True)
        
        for i in range(3):
            breath_placeholder.markdown(f"""
            <div class="breathing-container">
                <div class="breathing-circle circle-1"></div>
                <div class="breathing-circle circle-2"></div>
                <div class="breathing-circle circle-3"></div>
                <div class="breathing-circle circle-4"></div>
                <div class="breathing-circle circle-5"></div>
                <div class="breathing-circle circle-6"></div>
                <div class="breathing-text">
                    🫁 Breath {i+1}/3<br>
                    <span style="font-size: 1.2rem;">Inhale deeply...</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(4)
            
            breath_placeholder.markdown(f"""
            <div class="breathing-container">
                <div class="breathing-circle circle-1"></div>
                <div class="breathing-circle circle-2"></div>
                <div class="breathing-circle circle-3"></div>
                <div class="breathing-circle circle-4"></div>
                <div class="breathing-circle circle-5"></div>
                <div class="breathing-circle circle-6"></div>
                <div class="breathing-text">
                    🫁 Breath {i+1}/3<br>
                    <span style="font-size: 1.2rem;">Hold...</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(2)
            
            breath_placeholder.markdown(f"""
            <div class="breathing-container">
                <div class="breathing-circle circle-1"></div>
                <div class="breathing-circle circle-2"></div>
                <div class="breathing-circle circle-3"></div>
                <div class="breathing-circle circle-4"></div>
                <div class="breathing-circle circle-5"></div>
                <div class="breathing-circle circle-6"></div>
                <div class="breathing-text">
                    🫁 Breath {i+1}/3<br>
                    <span style="font-size: 1.2rem;">Exhale slowly...</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(4)
        
        breath_placeholder.success("✨ Breathing exercise completed! You feel more centered.")
        st.session_state.points += 10
        
        check_for_new_badges(st.session_state.points)
        
        st.balloons()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def show_pomodoro_section():
    """Pomodoro timer section with animated timer"""
    st.markdown('<h1 class="section-title">⏰ Pomodoro Study Timer</h1>', unsafe_allow_html=True)
    

    
    if st.session_state.timer_running and st.session_state.timer_seconds > 0:
        minutes = st.session_state.timer_seconds // 60
        seconds = st.session_state.timer_seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        total_seconds = 25 * 60 if st.session_state.timer_mode == 'focus' else 5 * 60
        progress = (total_seconds - st.session_state.timer_seconds) / total_seconds
        
        st.markdown(f"""
        <div class="pomodoro-timer-container">
            <div class="timer-circle">
                <div class="timer-progress" style="background: conic-gradient(from 0deg, transparent 0deg, rgba(255, 255, 255, 0.9) {progress * 360}deg);"></div>
                <div class="timer-text">{time_str}</div>
                <div class="timer-label">{st.session_state.timer_mode.title()} Time</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="pomodoro-timer-container">
            <div class="timer-circle">
                <div class="timer-progress" style="background: conic-gradient(from 0deg, transparent 0deg, rgba(255, 255, 255, 0.9) 0deg);"></div>
                <div class="timer-text">25:00</div>
                <div class="timer-label">Ready to Focus</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    .pomodoro-timer-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
        padding: 2rem;
    }
    
    .timer-circle {
        position: relative;
        width: 300px;
        height: 300px;
        border-radius: 50%;
        background: conic-gradient(from 0deg, #4ade80 0deg, #60a5fa 120deg, #f97316 240deg, #4ade80 360deg);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 20px 40px rgba(74, 222, 128, 0.3);
        animation: timerPulse 2s ease-in-out infinite;
    }
    
    @keyframes timerPulse {
        0%, 100% { transform: scale(1); box-shadow: 0 20px 40px rgba(74, 222, 128, 0.3); }
        50% { transform: scale(1.02); box-shadow: 0 25px 50px rgba(74, 222, 128, 0.4); }
    }
    
    .timer-progress {
        position: absolute;
        top: 10px;
        left: 10px;
        right: 10px;
        bottom: 10px;
        border-radius: 50%;
        background: conic-gradient(from 0deg, transparent 0deg, rgba(255, 255, 255, 0.9) 0deg);
        transition: all 0.3s ease;
        animation: progressRotate 1s linear infinite;
    }
    
    @keyframes progressRotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .timer-text {
        font-family: 'Fredoka One', cursive;
        font-size: 3rem;
        font-weight: bold;
        color: #1f2937;
        z-index: 10;
        text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.8);
        animation: textGlow 2s ease-in-out infinite;
    }
    
    @keyframes textGlow {
        0%, 100% { text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.8); }
        50% { text-shadow: 2px 2px 8px rgba(74, 222, 128, 0.6); }
    }
    
    .timer-label {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: #4a5568;
        margin-top: 10px;
        font-weight: 600;
        z-index: 10;
    }
    
    .timer-controls {
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-top: 2rem;
    }
    
    .timer-btn {
        background: linear-gradient(45deg, #4ade80, #60a5fa);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-family: 'Fredoka One', cursive;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(74, 222, 128, 0.3);
    }
    
    .timer-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(74, 222, 128, 0.4);
    }
    
    .timer-btn:active {
        transform: translateY(-1px);
    }
    
    .timer-btn.break {
        background: linear-gradient(45deg, #f97316, #60a5fa);
    }
    
    .timer-btn.break:hover {
        box-shadow: 0 12px 25px rgba(249, 115, 22, 0.4);
    }
    
    @media (prefers-color-scheme: dark) {
        .timer-text {
            color: #ffffff;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        }
        
        .timer-label {
            color: #d1d5db;
        }
        
        .timer-circle {
            background: conic-gradient(from 0deg, #4ade80 0deg, #60a5fa 120deg, #f97316 240deg, #4ade80 360deg);
            box-shadow: 0 20px 40px rgba(74, 222, 128, 0.4);
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Start Focus (25 min)", key="start_focus", use_container_width=True, disabled=st.session_state.timer_running):
            st.session_state.timer_running = True
            st.session_state.timer_mode = 'focus'
            st.session_state.timer_seconds = 25 * 60  # 25 minutes
            st.rerun()
    
    with col2:
        if st.button("☕ Start Break (5 min)", key="start_break", use_container_width=True, disabled=st.session_state.timer_running):
            st.session_state.timer_running = True
            st.session_state.timer_mode = 'break'
            st.session_state.timer_seconds = 5 * 60  # 5 minutes
            st.rerun()
    
    with col3:
        if st.button("⏹️ Stop Timer", key="stop_timer", use_container_width=True):
            st.session_state.timer_running = False
            st.session_state.timer_seconds = 0
            st.rerun()
    
    if not st.session_state.timer_running:
        st.info("⏰ Timer is ready! Click 'Start Focus' or 'Start Break' to begin a session.")
    
    if st.session_state.timer_running and st.session_state.timer_seconds > 0:
        current_time = time.time()
        if current_time - st.session_state.last_timer_update >= 1.0:
            st.session_state.timer_seconds -= 1
            st.session_state.last_timer_update = current_time
        
        st.empty()
        time.sleep(1)
        st.rerun()
    
    if st.session_state.timer_running and st.session_state.timer_seconds > 0:
        minutes = st.session_state.timer_seconds // 60
        seconds = st.session_state.timer_seconds % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        st.info(f"⏰ {st.session_state.timer_mode.title()} session in progress: {time_str}")
        
        if st.session_state.timer_seconds <= 0:
            st.session_state.timer_running = False
            st.session_state.pomodoro_completed += 1
            st.session_state.points += 20 if st.session_state.timer_mode == 'focus' else 10
            
            check_for_new_badges(st.session_state.points)
            
            st.success(f"🎉 {st.session_state.timer_mode.title()} session completed!")
            st.balloons()
            st.rerun()
    
    st.markdown('<div class="widget-card">', unsafe_allow_html=True)
    st.write("**💡 Break Activity Suggestions:**")
    
    for i, activity in enumerate(BREAK_ACTIVITIES[:5], 1):
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, rgba(74, 222, 128, 0.1), rgba(96, 165, 250, 0.1));
            padding: 12px;
            border-radius: 12px;
            margin: 8px 0;
            border-left: 3px solid #4ade80;
        ">
            <strong style="color: #4ade80;">{i}.</strong> <span style="color: #4a5568;">{activity}</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard_section():
    """Progress dashboard section"""
    st.markdown('<h1 class="section-title">📈 Progress Dashboard</h1>', unsafe_allow_html=True)
    
    if st.session_state.moods or st.session_state.screen_times:
        data = []
        max_len = max(len(st.session_state.moods), len(st.session_state.screen_times))
        
        for i in range(max_len):
            mood = st.session_state.moods[i] if i < len(st.session_state.moods) else None
            screen_time = st.session_state.screen_times[i] if i < len(st.session_state.screen_times) else None
            data.append({
                'Day': i + 1,
                'Mood': mood,
                'Screen Time': screen_time
            })
        
        df = pd.DataFrame(data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.session_state.moods:
                st.markdown('<div class="widget-card">', unsafe_allow_html=True)
                st.write("**😊 Mood Trends**")
                mood_data = df[df['Mood'].notna()]
                if not mood_data.empty:
                    st.line_chart(mood_data.set_index('Day')['Mood'])
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            if st.session_state.screen_times:
                st.markdown('<div class="widget-card">', unsafe_allow_html=True)
                st.write("**📱 Screen Time Trends**")
                screen_data = df[df['Screen Time'].notna()]
                if not screen_data.empty:
                    st.line_chart(screen_data.set_index('Day')['Screen Time'])
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="floating-widget">', unsafe_allow_html=True)
        st.write("**📊 Summary Statistics**")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.session_state.moods:
                avg_mood = sum(st.session_state.moods) / len(st.session_state.moods)
                st.metric("😊 Average Mood", f"{avg_mood:.1f}/10")
        
        with col2:
            if st.session_state.screen_times:
                avg_screen = sum(st.session_state.screen_times) / len(st.session_state.screen_times)
                st.metric("📱 Average Screen Time", f"{avg_screen:.1f} hours")
        
        with col3:
            st.metric("🌟 Total Calm Points", st.session_state.points)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="floating-widget">', unsafe_allow_html=True)
        st.info("📊 Start tracking your mood and screen time to see your progress here!")
        st.markdown('</div>', unsafe_allow_html=True)

def show_activities_section():
    """Activity suggestions section"""
    st.markdown('<h1 class="section-title">🎯 Activity Suggestions</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="widget-card">', unsafe_allow_html=True)
    st.write("**Here are some evidence-based activities to try during your breaks:**")
    
    for i, activity in enumerate(BREAK_ACTIVITIES, 1):
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.8); padding: 12px; border-radius: 12px; margin: 6px 0; border-left: 3px solid #4299e1; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <strong style="color: #1a202c;">{i}.</strong> <span style="color: #4a5568;">{activity}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown('<div class="floating-widget">', unsafe_allow_html=True)
    st.write("**🎲 Need a quick activity right now?**")
    
    if 'current_random_activity' not in st.session_state:
        st.session_state.current_random_activity = None
    
    if st.button("🎯 Pick Random Activity", key="random_activity_btn", use_container_width=True):
        st.session_state.current_random_activity = random.choice(BREAK_ACTIVITIES)
        st.session_state.points += 5
        
        check_for_new_badges(st.session_state.points)
        
        st.balloons()
        st.rerun()
    
    if st.session_state.current_random_activity:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #4ade80, #60a5fa);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 15px 0;
            text-align: center;
            box-shadow: 0 8px 25px rgba(74, 222, 128, 0.3);
            animation: cardPop 0.6s ease-out;
        ">
            <div style="font-size: 2rem; margin-bottom: 10px;">🎯</div>
            <div style="font-size: 1.3rem; font-weight: bold; margin-bottom: 10px;">Your Random Activity:</div>
            <div style="font-size: 1.1rem; line-height: 1.5;">{st.session_state.current_random_activity}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def show_badges_section():
    """Badges collection section"""
    st.markdown('<h1 class="section-title">🏆 Badges Collection</h1>', unsafe_allow_html=True)
    
    current_level, current_badges, badge_emojis = get_level_and_badges(st.session_state.points)
    
    all_badges = {
        "🌟 First Steps": {
            "emoji": "🌟",
            "requirement": "Earn 10 points",
            "description": "Complete your first wellness activities",
            "points_needed": 10
        },
        "📝 Journal Keeper": {
            "emoji": "📝",
            "requirement": "Write 3 gratitude entries",
            "description": "Start your gratitude journey",
            "points_needed": 30
        },
        "🎯 Goal Setter": {
            "emoji": "🎯",
            "requirement": "Earn 50 points",
            "description": "Show commitment to your wellness journey",
            "points_needed": 50
        },
        
        "🫁 Breath Master": {
            "emoji": "🫁",
            "requirement": "Complete 5 breathing exercises",
            "description": "Master the art of mindful breathing",
            "points_needed": 50
        },
        "⏰ Time Tracker": {
            "emoji": "⏰",
            "requirement": "Log mood and screen time for 7 days",
            "description": "Build consistent tracking habits",
            "points_needed": 70
        },
        "🧘‍♀️ Zen Master": {
            "emoji": "🧘‍♀️",
            "requirement": "Earn 100 points",
            "description": "Achieve a balanced state of mind",
            "points_needed": 100
        },
        "📊 Data Enthusiast": {
            "emoji": "📊",
            "requirement": "Track mood for 14 consecutive days",
            "description": "Show dedication to self-awareness",
            "points_needed": 120
        },
        "💭 Thoughtful Writer": {
            "emoji": "💭",
            "requirement": "Write 10 gratitude entries",
            "description": "Cultivate a grateful mindset",
            "points_needed": 130
        },
        
        "🎯 Focus Champion": {
            "emoji": "🎯",
            "requirement": "Complete 10 Pomodoro sessions",
            "description": "Master the art of focused work",
            "points_needed": 200
        },
        "💎 Wellness Warrior": {
            "emoji": "💎",
            "requirement": "Earn 200 points",
            "description": "Demonstrate exceptional dedication to wellness",
            "points_needed": 200
        },
        "🌱 Growth Mindset": {
            "emoji": "🌱",
            "requirement": "Earn 250 points",
            "description": "Embrace continuous personal development",
            "points_needed": 250
        },
        "👑 Mindfulness Guru": {
            "emoji": "👑",
            "requirement": "Earn 300 points",
            "description": "Reach the pinnacle of mindful living",
            "points_needed": 300
        },
        
        "🔥 Streak Master": {
            "emoji": "🔥",
            "requirement": "Log activities for 30 consecutive days",
            "description": "Maintain incredible consistency",
            "points_needed": 150
        },
        "🎨 Creative Soul": {
            "emoji": "🎨",
            "requirement": "Try 20 different random activities",
            "description": "Embrace creativity and spontaneity",
            "points_needed": 100
        },
        "🏃‍♀️ Early Bird": {
            "emoji": "🏃‍♀️",
            "requirement": "Complete 5 morning breathing exercises",
            "description": "Start your days mindfully",
            "points_needed": 50
        },
        "🌙 Night Owl": {
            "emoji": "🌙",
            "requirement": "Complete 5 evening breathing exercises",
            "description": "End your days peacefully",
            "points_needed": 50
        },
        "📱 Digital Balance": {
            "emoji": "📱",
            "requirement": "Track screen time for 21 days",
            "description": "Achieve healthy digital habits",
            "points_needed": 105
        },
        "💖 Self-Care Champion": {
            "emoji": "💖",
            "requirement": "Complete 15 wellness activities",
            "description": "Prioritize your well-being",
            "points_needed": 150
        },
        "🎯 Precision Tracker": {
            "emoji": "🎯",
            "requirement": "Log mood with perfect accuracy for 10 days",
            "description": "Master emotional awareness",
            "points_needed": 50
        },
        "🧠 Mental Fitness": {
            "emoji": "🧠",
            "requirement": "Complete 20 breathing exercises",
            "description": "Build mental resilience",
            "points_needed": 200
        },
        "⏱️ Time Management": {
            "emoji": "⏱️",
            "requirement": "Complete 25 Pomodoro sessions",
            "description": "Become a productivity expert",
            "points_needed": 500
        },
        "📚 Knowledge Seeker": {
            "emoji": "📚",
            "requirement": "Read all How to Use sections",
            "description": "Commit to learning and growth",
            "points_needed": 50
        },
        "🌟 Gratitude Guru": {
            "emoji": "🌟",
            "requirement": "Write 25 gratitude entries",
            "description": "Master the art of gratitude",
            "points_needed": 250
        },
        "🎪 Activity Explorer": {
            "emoji": "🎪",
            "requirement": "Try 50 different random activities",
            "description": "Embrace life's variety",
            "points_needed": 250
        },
        "🏆 Consistency King": {
            "emoji": "🏆",
            "requirement": "Log activities for 60 consecutive days",
            "description": "Show extraordinary dedication",
            "points_needed": 300
        },
        "💎 Diamond Mind": {
            "emoji": "💎",
            "requirement": "Earn 500 points",
            "description": "Achieve diamond-level wellness",
            "points_needed": 500
        },
        "👑 Wellness Legend": {
            "emoji": "👑",
            "requirement": "Earn 750 points",
            "description": "Become a wellness legend",
            "points_needed": 750
        },
        "⭐ Superstar": {
            "emoji": "⭐",
            "requirement": "Earn 1000 points",
            "description": "Reach superstar status",
            "points_needed": 1000
        },
        "🌟 Legendary Master": {
            "emoji": "🌟",
            "requirement": "Earn 1500 points",
            "description": "Achieve legendary mastery",
            "points_needed": 1500
        },
        "🏅 Ultimate Champion": {
            "emoji": "🏅",
            "requirement": "Earn 2000 points",
            "description": "Become the ultimate wellness champion",
            "points_needed": 2000
        },
        "💫 Cosmic Master": {
            "emoji": "💫",
            "requirement": "Earn 2500 points",
            "description": "Transcend to cosmic wellness mastery",
            "points_needed": 2500
        },
        "👑 Immortal Legend": {
            "emoji": "👑",
            "requirement": "Earn 3000 points",
            "description": "Achieve immortal wellness legend status",
            "points_needed": 3000
        },
        "🌟 Divine Master": {
            "emoji": "🌟",
            "requirement": "Earn 5000 points",
            "description": "Reach divine wellness mastery",
            "points_needed": 5000
        },
        "✨ Eternal Champion": {
            "emoji": "✨",
            "requirement": "Earn 10000 points",
            "description": "Become an eternal wellness champion",
            "points_needed": 10000
        }
    }
    
    st.markdown('<div class="floating-widget">', unsafe_allow_html=True)
    st.write("**✅ Badges You've Earned:**")
    
    if current_badges:
        for badge in current_badges:
            badge_info = all_badges[badge]
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
                color: rgb(0, 0, 0) !important;
                padding: 15px;
                border-radius: 15px;
                margin: 10px 0;
                border: 2px solid #c3e6cb;
                box-shadow: 0 4px 15px rgba(195, 230, 203, 0.3);
            ">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="font-size: 2rem;">{badge_info['emoji']}</div>
                    <div>
                        <div style="font-weight: bold; font-size: 1.1rem; color: rgb(0, 0, 0) !important;">{badge}</div>
                        <div style="font-size: 0.9rem; opacity: 0.8; color: rgb(0, 0, 0) !important;">{badge_info['description']}</div>
                        <div style="font-size: 0.8rem; opacity: 0.7; margin-top: 5px; color: rgb(0, 0, 0) !important;">{badge_info['requirement']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No badges earned yet. Start your wellness journey to earn your first badge!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="widget-card">', unsafe_allow_html=True)
    st.write("**🎯 Badges to Unlock:**")
    
    unearned_badges = [badge for badge in all_badges.keys() if badge not in current_badges]
    
    if unearned_badges:
        for badge in unearned_badges:
            badge_info = all_badges[badge]
            points_needed = badge_info['points_needed'] - st.session_state.points
            progress_percent = min(100, (st.session_state.points / badge_info['points_needed']) * 100)
            
            st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.8);
                padding: 15px;
                border-radius: 15px;
                margin: 10px 0;
                border: 2px solid #e5e7eb;
                display: flex;
                align-items: center;
                gap: 15px;
            ">
                <div style="font-size: 2rem; opacity: 0.5;">{badge_info['emoji']}</div>
                <div style="flex-grow: 1;">
                    <div style="font-weight: bold; color: rgb(0, 0, 0) !important; font-size: 1.1rem;">{badge}</div>
                    <div style="color: rgb(0, 0, 0) !important; font-size: 0.9rem;">{badge_info['description']}</div>
                    <div style="color: rgb(0, 0, 0) !important; font-size: 0.8rem; margin-top: 5px;">{badge_info['requirement']}</div>
                    <div style="margin-top: 8px;">
                        <div style="background: #e5e7eb; border-radius: 10px; height: 8px; overflow: hidden;">
                            <div style="background: linear-gradient(90deg, #1a5f3c, #2d5a3d); width: {progress_percent}%; height: 100%; transition: width 0.5s ease;"></div>
                        </div>
                        <div style="color: rgb(0, 0, 0) !important; font-size: 0.8rem; margin-top: 3px;">
                            {st.session_state.points}/{badge_info['points_needed']} points ({progress_percent:.1f}%)
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("🎉 Congratulations! You've earned all available badges!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="floating-widget">', unsafe_allow_html=True)
    st.write("**💡 Tips to Earn Badges Faster:**")
    st.markdown("""
    <div style="background: rgba(255,255,255,0.95); padding: 15px; border-radius: 15px; margin: 10px 0; border-left: 4px solid #1a5f3c;">
        <ul style="color: rgb(0, 0, 0) !important; margin: 0; padding-left: 20px;">
            <li><strong>Log your mood daily</strong> - 5 points each time</li>
            <li><strong>Track your screen time</strong> - 5 points each time</li>
            <li><strong>Write gratitude entries</strong> - 10 points each time</li>
            <li><strong>Complete breathing exercises</strong> - 10 points each time</li>
            <li><strong>Finish Pomodoro sessions</strong> - 20 points each time</li>
            <li><strong>Try random activities</strong> - 5 points each time</li>
            <li><strong>Consistent tracking</strong> - Earn streak bonuses!</li>
            <li><strong>Multiple activities</strong> - Unlock special achievement badges!</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def get_fallback_response(user_input):
    user_input_lower = user_input.lower()
    
    if any(word in user_input_lower for word in ['sad', 'depressed', 'down', 'unhappy', 'miserable']):
        return "I'm sorry you're feeling down. Remember that it's okay to not be okay. Try taking a few deep breaths, going for a short walk, or talking to someone you trust. You're not alone in this. 💙"
    
    elif any(word in user_input_lower for word in ['anxious', 'worried', 'stress', 'nervous', 'panic']):
        return "Anxiety can be really overwhelming. Try the 4-7-8 breathing technique: inhale for 4, hold for 7, exhale for 8. Also, remember that most worries don't come true. You're stronger than you think! 🌟"
    
    elif any(word in user_input_lower for word in ['tired', 'exhausted', 'burnout', 'overwhelmed']):
        return "It sounds like you need some rest. Try taking a 20-minute break, doing something you enjoy, or just sitting quietly. It's okay to pause and recharge. You deserve it! 😌"
    
    elif any(word in user_input_lower for word in ['happy', 'good', 'great', 'excited', 'joy']):
        return "That's wonderful! I'm so glad you're feeling good. Remember to savor these moments and maybe share your joy with someone else. Positive energy is contagious! ✨"
    
    elif any(word in user_input_lower for word in ['help', 'support', 'advice']):
        return "I'm here to listen and support you. Remember that professional help is always available if you need it. You're taking a great step by reaching out. What's on your mind? 🤗"
    
    elif any(word in user_input_lower for word in ['study', 'work', 'school', 'exam', 'test']):
        return "Academic stress is real! Try breaking your work into smaller chunks, take regular breaks, and remember that your worth isn't defined by grades. You're doing your best! 📚"
    
    else:
        return "Thank you for sharing that with me. I'm here to listen and support you. Remember that your feelings are valid and you're doing great just by being here. Is there anything specific you'd like to talk about? 💙"

def show_chatbot_section():
    st.markdown('<h1 class="section-title">💬 Therapy Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<div class="widget-card">', unsafe_allow_html=True)
    st.write("This supportive chatbot is here to listen and provide gentle encouragement. All conversations are private and not stored.")
    

    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    for msg in st.session_state.chat_history:
        st.chat_message(msg['role']).write(msg['content'])
    
    user_input = st.chat_input("How are you feeling today? Or ask for support...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("Therapist is typing..."):
            try:
                client = openai.OpenAI(api_key=OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a supportive, empathetic, and non-judgmental mental health therapist for students. Keep responses short, positive, and actionable. Never give medical advice or diagnosis."},
                        *st.session_state.chat_history
                    ],
                    max_tokens=200,
                    temperature=0.7
                )
                bot_reply = response.choices[0].message.content
            except Exception as e:
                bot_reply = get_fallback_response(user_input)
        
        st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
        st.chat_message("assistant").write(bot_reply)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
