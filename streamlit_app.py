import pandas as pd
import psycopg2
import streamlit as st

st.set_page_config(page_title="madang 주문 조회", page_icon="📚")
st.title("madang 주문 조회")


def run_query(name: str) -> pd.DataFrame:
    sql = """
        select o.orderid, c.name, b.bookname, o.saleprice, o.orderdate
        from Customer c, Orders o, Book b
        where c.name = %s and c.custid = o.custid and b.bookid = o.bookid
        order by o.orderid;
    """
    conn = psycopg2.connect(st.secrets["DATABASE_URL"])
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (name,))
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
    finally:
        conn.close()
    return pd.DataFrame(rows, columns=cols)


col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
with col1:
    name = st.text_input("고객 이름", value="박지성")
with col2:
    clicked = st.button("Search", use_container_width=True)

if clicked:
    try:
        result = run_query(name.strip())
    except Exception as e:
        st.error(f"DB 접속/조회 중 오류가 발생했어요: {e}")
    else:
        if result.empty:
            st.info("해당 고객의 주문 내역이 없어요.")
        else:
            st.dataframe(result, use_container_width=True, hide_index=True)
