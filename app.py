import streamlit as st
import yfinance as yf

# 1. 앱 제목 설정
st.set_page_config(page_title="주가 최고점 모니터링", page_icon="📉")
st.title("📉 주가 최고점 & 하락률 계산기")

# 2. 사용자 입력창 만들기 (핵심 기능!)
st.write("궁금한 주식의 티커를 입력해보세요.")
ticker_input = st.text_input("미국 주식(예: QLD, AAPL) 또는 한국 주식(예: 005930.KS)", "QLD")
ticker_symbol = ticker_input.upper() # 소문자로 쳐도 대문자로 자동 변환

with st.spinner(f'{ticker_symbol} 데이터를 불러오는 중입니다...'):
    ticker_data = yf.Ticker(ticker_symbol)
    # 최근 5년간의 데이터를 불러옵니다 (기간은 '1y', 'max' 등으로 변경 가능)
    df = ticker_data.history(period="5y") 

if not df.empty:
    # 3. 데이터 계산하기
    current_price = df['Close'].iloc[-1] # 가장 최근 종가
    
    max_price = df['Close'].max() # 기간 내 최고가
    # 최고가를 기록한 날짜를 찾아 보기 좋은 형식으로 변경
    max_date = df['Close'].idxmax().strftime('%Y년 %m월 %d일') 
    
    # 증감률(하락률) 계산
    drawdown = ((current_price - max_price) / max_price) * 100
    
    # 4. 화면에 결과 보여주기
    st.subheader(f"📊 {ticker_symbol} 핵심 지표 요약")
    
    # 2x2 형태로 깔끔하게 배치
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="기간 내 최고가", value=f"{max_price:.2f}")
        st.metric(label="현재가", value=f"{current_price:.2f}")
    with col2:
        st.metric(label="최고가 기록일", value=max_date)
        # 하락률은 색상으로 직관적으로 표시되도록 metric 기능 활용
        st.metric(label="최고가 대비 증감률", value=f"{drawdown:.2f}%")
        
    st.subheader("📈 최근 5년 주가 흐름")
    st.line_chart(df['Close'])
    
else:
    st.error("데이터를 찾을 수 없습니다. 티커를 다시 확인해주세요. (한국 주식은 코스피 .KS, 코스닥 .KQ를 붙여야 합니다)")
