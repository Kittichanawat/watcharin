import random

# กำหนดระดับตัวละครตามจำนวนดาวและความน่าจะเป็นในการสุ่ม
character_star = {
    "5 ดาว": 0.01,   # 1% โอกาสที่จะได้ตัวละคร 5 ดาว
    "4 ดาว": 0.05,   # 5% โอกาสที่จะได้ตัวละคร 4 ดาว
    "3 ดาว": 0.15,   # 15% โอกาสที่จะได้ตัวละคร 3 ดาว
    "2 ดาว": 0.30,   # 30% โอกาสที่จะได้ตัวละคร 2 ดาว
    "1 ดาว": 0.49    # 49% โอกาสที่จะได้ตัวละคร 1 ดาว
}

# ฟังก์ชันในการสุ่มตัวละครโดยใช้ Monte Carlo
def monte_carlo_draw(distribution, guaranteed_5_star=False, force_5_star=False):
    if guaranteed_5_star:
        return "5 ดาวหน้าตู้สุ่ม"  # การันตีตัวละคร 5 ดาวหน้าตู้สุ่ม เมื่อถึงครั้งที่ 90
    if force_5_star:
        return "5 ดาวหน้าตู้สุ่ม"  # บังคับให้ได้ "5 ดาวหน้าตู้สุ่ม" ถ้ามีการสุ่มหลุดเรทครั้งก่อนหน้า

    rand_num = random.random()  # สุ่มตัวเลขระหว่าง 0 ถึง 1
    cumulative_probability = 0.0
    
    # วนลูปตามความน่าจะเป็นของระดับตัวละครแต่ละตัว
    for stars, probability in distribution.items():
        cumulative_probability += probability
        if rand_num < cumulative_probability:
            if stars == "5 ดาว":
                # สุ่ม 50/50 ว่าจะออก "5 ดาวหน้าตู้สุ่ม" หรือ "5 ดาวหลุดเรท"
                return "5 ดาวหน้าตู้สุ่ม" if random.random() < 0.5 else "5 ดาวหลุดเรท"
            return stars

# ทดสอบการสุ่มตัวละครหลายครั้ง
def simulate_draws(num_draws, distribution):
    results = {
        "5 ดาวหน้าตู้สุ่ม": 0,
        "5 ดาวหลุดเรท": 0,
        "4 ดาว": 0,
        "3 ดาว": 0,
        "2 ดาว": 0,
        "1 ดาว": 0
    }  # สร้าง dict เพื่อเก็บผลลัพธ์
    got_5_star = False  # ตัวแปรเพื่อตรวจสอบว่ามีการได้ตัวละคร 5 ดาวหรือยัง
    guarantee_count = 0  # ตัวแปรนับจำนวนครั้งที่การันตีตัวละคร 5 ดาว
    force_next_5_star = False  # ตัวแปรเพื่อบังคับให้ได้ "5 ดาวหน้าตู้สุ่ม" ครั้งถัดไปหลังจากได้ "5 ดาวหลุดเรท"

    for i in range(1, num_draws + 1):
        # การันตีตัวละคร 5 ดาวหน้าตู้สุ่มในครั้งที่ 90 ถ้ายังไม่ได้มาก่อน
        stars = monte_carlo_draw(distribution, guaranteed_5_star=(i == 90 and not got_5_star), force_5_star=force_next_5_star)
        
        # รีเซ็ต force_next_5_star หลังจากใช้บังคับให้ได้ 5 ดาวหน้าตู้
        if force_next_5_star:
            force_next_5_star = False

        # นับจำนวนครั้งที่ได้ตัวละครระดับต่างๆ
        results[stars] += 1
        
        if stars in ["5 ดาวหน้าตู้สุ่ม", "5 ดาวหลุดเรท"]:
            got_5_star = True
            guarantee_count += (i == 90)  # เพิ่มจำนวนครั้งที่การันตีถ้าเป็นครั้งที่ 90
            
            if stars == "5 ดาวหลุดเรท":
                # ถ้าได้ "5 ดาวหลุดเรท" บังคับให้ครั้งถัดไปได้ "5 ดาวหน้าตู้สุ่ม"
                force_next_5_star = True

    return results, guarantee_count

# จำนวนครั้งในการสุ่ม (เช่น 1000 ครั้ง)
num_draws = 100000
results, guarantee_count = simulate_draws(num_draws, character_star)

# แสดงผลการสุ่ม
results_output = {stars: (count, (count / num_draws) * 100) for stars, count in results.items()}
guarantee_count_output = guarantee_count

for stars, (count, percentage) in results_output.items():
    print(f"{stars}: {count} ครั้ง ({percentage:.2f}%)")

print(f"จำนวนครั้งที่การันตีตัวละคร 5 ดาวเมื่อผู้ใช้สุ่มถึง90ครั้ง: {guarantee_count_output} ครั้ง")
