import streamlit as st
import yfinance as yf

# 1. 앱 제목 및 기본 설정
st.set_page_config(page_title="QLD 위험도 모니터링", page_icon="📉")
st.title("📉 QLD 주가 & MDD 대시보드")
st.write("2025년 1월 1일 이후의 최고가 대비 최대 낙폭(MDD)을 계산합니다.")

# 2. 데이터 불러오기 설정
ticker_symbol = "QLD"
start_date = "2025-01-01"

# 사용자에게 데이터 로딩 중임을 알려주는 기능
with st.spinner('미국 주식 데이터를 불러오는 중입니다...'):
    ticker_data = yf.Ticker(ticker_symbol)
    df = ticker_data.history(start=start_date)

# 데이터가 정상적으로 불러와졌는지 확인
if not df.empty:
    # 3. 핵심 로직 계산
    # 가장 최근 종가 (현재가)
    current_price = df['Close'].iloc[-1]
    
    # 누적 최고가 계산 (과거부터 현재까지의 가장 높았던 가격 갱신)
    df['Roll_Max'] = df['Close'].cummax()
    
    # 고점 대비 하락률(Drawdown) 계산: ((현재가 - 최고가) / 최고가) * 100
    df['Drawdown'] = (df['Close'] / df['Roll_Max'] - 1) * 100
    
    # 최대 낙폭(MDD) 추출 (가장 많이 떨어진 수치)
    mdd = df['Drawdown'].min()
    
    # 4. 모바일 친화적 UI 화면 구성
    st.subheader("📊 핵심 지표 요약")
    
    # 화면을 두 칸으로 나누어 수치를 나란히 배치
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="현재 종가", value=f"${current_price:.2f}")
    with col2:
        # MDD는 직관적으로 볼 수 있게 표시
        st.metric(label="25년 이후 MDD", value=f"{mdd:.2f}%")
        
    # 5. 시각화 차트 추가
    st.subheader("📈 25년 이후 주가 흐름")
    st.line_chart(df['Close'])
    
    st.subheader("📉 하락폭(Drawdown) 추이")
    # 하락률만 따로 모아 차트로 보여주어 위험도를 시각화
    st.line_chart(df['Drawdown'])
    
else:
    # 데이터를 못 불러왔을 때의 에러 메시지
    st.error("데이터를 불러오지 못했습니다. 잠시 후 다시 시도해주세요.")
