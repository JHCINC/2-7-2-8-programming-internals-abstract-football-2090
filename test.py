import random


attack_abilities = [10, 10, 10, 10]
attacker_amount = len(attack_abilities)
defence_abilities = [10, 10, 10, 10]
defender_amount = len(defence_abilities)
attack_modifies = [1, 1, 1, 1]
defence_modifies = [1, 1, 1, 1]


def calculate_average(function, times):
    result = 0
    for _ in range(times):
        result += function()
    print(result / times)


def advance():
    advance_result = 0
    defence_rolls = [random.randrange(0, 7) + random.randrange(0, 7) for _ in range(defender_amount)]

    for attacker in range(attacker_amount):
        attack_efficiency = 1
        attack_ability = attack_abilities[attacker]
        attack_modify = attack_modifies[attacker]
        attack_roll = random.randrange(0, 8) + random.randrange(0, 8)
        attack_expectation = 2 + 0.25 * attack_ability * attack_modify

        print('球员发起进攻，能力：' + str(attack_ability) + ' 骰点：' + str(attack_roll) + ' 期望：' + str(attack_expectation))

        for defender in range(defender_amount):
            defence_ability = defence_abilities[defender]
            defence_modify = defence_modifies[defender]
            defence_roll = defence_rolls[defender]
            defence_result = 0

            if (defence_ability + defence_roll) >= (attack_ability + attack_roll):
                defence_result = (0.1 + defence_ability * 0.02) * defence_modify
                attack_efficiency -= defence_result

            print('球员防守，能力：' + str(defence_ability) + ' 骰点：' + str(defence_roll) + ' 防守成果：' + str(defence_result))

        if attack_efficiency > 0:
            attack_result = attack_efficiency * attack_expectation
            advance_result += attack_result
            print('进攻成功，效率：' + str(attack_efficiency), ' 成果：' + str(attack_result))
        else:
            print('进攻失败')

        print()

    random_modify = random.randint(0, 5)
    advance_result = round(advance_result + random_modify)
    print('修正值： ' + str(random_modify))
    print('进攻总成果：' + str(advance_result))

    return advance_result


def tackle():
    attack_rolls = [random.randint(0, 10) for _ in range(attacker_amount)]

    for defender in range(defender_amount):
        tackle_difficulty = 0
        defence_ability = defence_abilities[defender]
        defence_modify = defence_modifies[defender]
        defence_roll = random.randint(0, 7)

        print('球员发起抢断，能力：' + str(defence_ability) + ' 骰点：' + str(defence_roll))

        for attacker in range(attacker_amount):
            attack_ability = attack_abilities[attacker]
            attack_modify = attack_modifies[attacker]
            attack_roll = attack_rolls[attacker]

            print('球员控球，能力：' + str(attack_ability) + ' 骰点：' + str(attack_roll))

            if attack_ability + attack_roll >= defence_ability + defence_roll:
                difficulty_increase = (20 + attack_ability) * attack_modify
                tackle_difficulty += difficulty_increase
                print('抢断无优势，抢断难度增加：' + str(difficulty_increase))
            else:
                difficulty_increase = ((20 + attack_ability) * attack_modify) * 0.2
                tackle_difficulty += difficulty_increase
                print('抢断有优势，抢断难度增加：' + str(difficulty_increase))

        tackle_possibility = ((1.5 + defence_ability * 0.3) * defence_modify) / tackle_difficulty
        if random.random() < tackle_possibility:
            print('球员抢断成功')
            return 1

    print('抢断最终失败')
    return 0

calculate_average(tackle, 10000)
