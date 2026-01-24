import flet as ft
import random

# --- [1. 파일 규칙 및 수치 완벽 이식] ---
INITIAL_TEMP = 15.0
GOAL_TEMP = 20.0
TOTAL_ROUNDS = 7
CHOICE_OPTIONS = {
    1: {"name": "경제성장", "gp": 15, "color": "#E74C3C"}, #
    2: {"name": "균형성장", "gp": 10, "color": "#F39C12"}, #
    3: {"name": "환경보전", "gp": 8, "color": "#27AE60"}   #
}

def main(page: ft.Page):
    page.title = "Climate Dilemma: Master Edition"
    page.window_width = 1100
    page.window_height = 850
    page.bgcolor = "#FFFFFF"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT

    # 게임 상태 관리
    st = {
        "temp": INITIAL_TEMP,
        "round": 1,
        "nations": {},
        "is_game_over": False,
        "actual": {}
    }

    def init_game_data():
        st["temp"] = INITIAL_TEMP
        st["round"] = 1
        st["is_game_over"] = False
        st["nations"] = {
            '대한민국': {"gp": 20, "env_count": 0, "plan": ""},
            '미국': {"gp": 25, "env_count": 0, "plan": ""},
            '스웨덴': {"gp": 18, "env_count": 0, "plan": ""},
            '투발루': {"gp": 15, "env_count": 0, "plan": ""}
        }

    init_game_data()

    # UI 컴포넌트 선언
    temp_display = ft.Text(f"{st['temp']:.2f}°C", size=50, weight="bold", color="#2D3436")
    round_info = ft.Text(f"ROUND {st['round']} / 7", size=24, weight="bold", color="#2980B9")
    gp_info = ft.Text(f"내 자산: {st['nations']['대한민국']['gp']} GP", size=22, weight="bold")
    nation_list_ui = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    # [롤스크린 핵심] 원본 설정 그대로 유지
    log_column = ft.Column(spacing=8, scroll=ft.ScrollMode.ALWAYS, auto_scroll=True)
    log_column.expand = True 

    # 리플레이 기능
    def reset_game(e):
        init_game_data()
        log_column.controls.clear()
        choice_buttons.disabled = False
        update_ui()
        write_log("🔄 게임을 다시 시작합니다!", color="#2980B9", bold=True)
        start_round()

    # 원본 하단 버튼에서 검증된 Container 방식으로 생성
    replay_btn = ft.Container(
        content=ft.Text("🔄 Replay", size=14, weight="bold", color="#636E72"),
        on_click=reset_game,
        padding=5,
        border_radius=5
    )

    left_panel = ft.Container(
        content=ft.Column([
            round_info,
            ft.Divider(height=20, color="transparent"),
            ft.Text("현재 지구 온도", size=18, weight="bold"),
            temp_display,
            gp_info,
            ft.Divider(height=40),
            ft.Text("🌍 국가별 약속", size=20, weight="bold"),
            nation_list_ui
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=30, border_radius=30, bgcolor="#F1F2F6", width=380
    )

    # [로그창 레이아웃 수정] 롤스크린 바가 패널 우측 끝에 붙도록 패딩 미세 조정
    right_panel = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("활동 로그", size=14, color="#636E72", weight="bold"),
                replay_btn
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(height=10),
            log_column # expand=True가 적용된 롤스크린 로그
        ], expand=True),
        expand=True, 
        padding=ft.Padding(30, 30, 10, 30), # 우측 패딩을 10으로 줄여 스크롤바를 바깥으로 밀어냄
        bgcolor="#F8F9FA", 
        border_radius=30,
        border=ft.Border.all(2, "#DFE4EA")
    )

    def write_log(msg, color="#2D3436", bold=False, size=16):
        log_column.controls.append(ft.Text(msg, color=color, size=size, weight="bold" if bold else "normal"))
        page.update()

    def update_ui():
        temp_display.value = f"{st['temp']:.2f}°C"
        round_info.value = f"ROUND {st['round']} / 7"
        gp_info.value = f"내 자산: {st['nations']['대한민국']['gp']} GP"
        
        if st['temp'] >= 19.0: 
            left_panel.bgcolor = "#FFCCCC"; temp_display.color = "#FF0000"
        elif st['temp'] >= 17.5: 
            left_panel.bgcolor = "#FFE5CC"; temp_display.color = "#FF8000"
        else: 
            left_panel.bgcolor = "#F1F2F6"; temp_display.color = "#2D3436"

        nation_list_ui.controls.clear()
        for name, data in st['nations'].items():
            if name == '대한민국': continue
            nation_list_ui.controls.append(
                ft.Text(f"{name}: {data['plan']}", size=16, weight="bold", color="#636E72")
            )
        page.update()

    def start_round():
        if st['round'] > TOTAL_ROUNDS: return
        is_lie_round = (st['round'] % 2 == 0)
        write_log("-" * 45)
        write_log(f"📍 [제 {st['round']} 라운드 국제 협상]", bold=True, size=18)
        
        if is_lie_round:
            write_log("🚨 알림: 이번 라운드는 타국이 거짓 약속을 할 수 있습니다!", color="#E74C3C", bold=True)

        for name in ['미국', '스웨덴', '투발루']:
            real = random.choices([1, 2, 3], weights=[4, 3, 3])[0]
            st['actual'][name] = real
            if is_lie_round and random.random() < 0.8:
                st['nations'][name]['plan'] = "3번(환경보전)"
            else:
                st['nations'][name]['plan'] = f"{real}번"
            write_log(f" > {name} 약속: \"이번엔 {st['nations'][name]['plan']}!\"")
        update_ui()

    def handle_choice(e):
        if st['is_game_over']: return
        player_choice = e.control.data
        st['actual']['대한민국'] = player_choice
        
        write_log(f"\n📢 라운드 결과 발표", bold=True, size=18)
        round_gp_sum = 0
        
        for name in ['대한민국', '미국', '스웨덴', '투발루']:
            choice = st['actual'][name]
            gain = CHOICE_OPTIONS[choice]['gp']
            disaster_penalty = 0
            if st['temp'] >= 18.5 and choice == 1:
                disaster_penalty = -8
                write_log(f" 💀 {name}: 기후 재앙으로 인한 피해 발생! (-8 GP)", color="#C0392B", bold=True)

            st['nations'][name]['gp'] += (gain + disaster_penalty)
            round_gp_sum += gain
            if choice == 3: st['nations'][name]['env_count'] += 1

            if name == '대한민국':
                write_log(f" ● 나: {choice}번 선택 (+{gain + disaster_penalty} GP)", bold=True)
            else:
                status = ""
                if (st['round'] % 2 == 0):
                    is_honest = st['nations'][name]['plan'].startswith(str(choice))
                    status = " [정직]" if is_honest else " [배신! ❌]"
                write_log(f" ○ {name}: {choice}번 선택{status} (+{gain + disaster_penalty} GP)")

        if round_gp_sum >= 50: change = 1.8
        elif round_gp_sum >= 40: change = 1.0
        elif round_gp_sum >= 35: change = 0.3
        elif round_gp_sum >= 30: change = -0.1
        else: change = -0.5

        if st['actual'].get('미국') == 3: change -= 0.1
        if st['actual'].get('스웨덴') == 3: change -= 0.1
        
        st['temp'] += change
        write_log(f"🌡️ 온도 변화: {change:+.2f}°C", color="#E74C3C" if change > 0 else "#27AE60")
        update_ui()

        if st['temp'] >= GOAL_TEMP:
            end_game(False)
        elif st['round'] == TOTAL_ROUNDS:
            end_game(True)
        else:
            st['round'] += 1
            start_round()

    def end_game(success):
        st['is_game_over'] = True
        write_log("\n" + "="*45)
        write_log("📜 최종 기후 위기 결과 보고서", size=22, bold=True)
        write_log("="*45)
        
        if success:
            write_log(f"🕊️ 인류 생존 성공! 최종 온도: {st['temp']:.2f}°C", color="#27AE60", bold=True, size=18)
            bonus_pool = int((20.0 - st['temp']) * 60)
            total_env = sum(n['env_count'] for n in st['nations'].values())
            if total_env > 0:
                write_log(f"\n🎁 환경 기여 보너스 분배 (총액: {bonus_pool} GP)", bold=True)
                for name, data in st['nations'].items():
                    bonus = int((data['env_count'] / total_env) * bonus_pool)
                    data['gp'] += bonus
                    if bonus > 0: write_log(f"  - {name}: +{bonus} GP 獲得")

            winner = max(st['nations'], key=lambda x: st['nations'][x]['gp'])
            write_log(f"\n🏆 최종 우승 국가: [{winner}]", color="#F39C12", size=26, bold=True)
        else:
            write_log(f"🌋 임계점 도달! 인류가 멸망했습니다.", color="#E74C3C", bold=True, size=18)
            write_log(f"최종 온도: {st['temp']:.2f}°C", color="#E74C3C")

        write_log("\n[국가별 최종 자산 현황]")
        for name, data in st['nations'].items():
            write_log(f" - {name}: {data['gp']} GP")
            
        choice_buttons.disabled = True
        page.update()

    # 하단 선택 버튼 (원본 스타일 유지)
    choice_buttons = ft.Row(
        controls=[
            ft.Container(
                content=ft.Text(f"{opt['name']}\n+{opt['gp']}GP", color="white", weight="bold", size=18, text_align=ft.TextAlign.CENTER),
                bgcolor=opt['color'], padding=20, border_radius=15, on_click=handle_choice, data=k, expand=True,
                alignment=ft.Alignment(0, 0)
            ) for k, opt in CHOICE_OPTIONS.items()
        ],
        spacing=15
    )

    page.add(
        ft.Row([left_panel, right_panel], expand=True, spacing=20),
        ft.Container(choice_buttons, padding=10)
    )

    start_round()

if __name__ == "__main__":
    ft.run(main)
