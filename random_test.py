import random

# กำหนดระดับตัวละครตามจำนวนดาวและความน่าจะเป็นในการสุ่ม
star_distribution = {
    "5 ดาว": 0.01,  # 1% โอกาสที่จะได้ตัวละคร 5 ดาว
    "4 ดาว": 0.05,  # 5% โอกาสที่จะได้ตัวละคร 4 ดาว
    "3 ดาว": 0.15,  # 15% โอกาสที่จะได้ตัวละคร 3 ดาว
    "2 ดาว": 0.30,  # 30% โอกาสที่จะได้ตัวละคร 2 ดาว
    "1 ดาว": 0.49   # 49% โอกาสที่จะได้ตัวละคร 1 ดาว
}

# ฟังก์ชันในการสุ่มตัวละครโดยใช้ Monte Carlo
def monte_carlo_draw(distribution, guaranteed_5_star=False):
    if guaranteed_5_star:
        return "5 ดาว"  # การันตีตัวละคร 5 ดาว เมื่อถึงครั้งที่ 90
    
    rand_num = random.random()  # สุ่มตัวเลขระหว่าง 0 ถึง 1
    cumulative_probability = 0.0
    
    # วนลูปตามความน่าจะเป็นของระดับตัวละครแต่ละตัว
    for stars, probability in distribution.items():
        cumulative_probability += probability
        if rand_num < cumulative_probability:
            return stars

# ทดสอบการสุ่มตัวละครหลายครั้ง
def simulate_draws(num_draws, distribution):
    results = {stars: 0 for stars in distribution}  # สร้าง dict เพื่อเก็บผลลัพธ์
    got_5_star = False  # ตัวแปรเพื่อตรวจสอบว่ามีการได้ตัวละคร 5 ดาวหรือยัง
    guarantee_count = 0  # ตัวแปรนับจำนวนครั้งที่การันตีตัวละคร 5 ดาว
    
    for i in range(1, num_draws + 1):
        # การันตีตัวละคร 5 ดาวในครั้งที่ 90 ถ้ายังไม่ได้มาก่อน
        stars = monte_carlo_draw(distribution, guaranteed_5_star=(i == 90 and not got_5_star))
        results[stars] += 1  # นับจำนวนครั้งที่ได้ตัวละครระดับต่างๆ
        
        if stars == "5 ดาว":
            got_5_star = True
            guarantee_count += (i == 90)  # เพิ่มจำนวนครั้งที่การันตีถ้าเป็นครั้งที่ 90
    
    return results, guarantee_count

# จำนวนครั้งในการสุ่ม (เช่น 100 ครั้ง)
num_draws = 900
results, guarantee_count = simulate_draws(num_draws, star_distribution)

# แสดงผลการสุ่ม
for stars, count in results.items():
    print(f"{stars}: {count} times ({(count / num_draws) * 100:.2f}%)")

print(f"จำนวนครั้งที่การันตีตัวละคร 5 ดาว: {guarantee_count} ครั้ง")
