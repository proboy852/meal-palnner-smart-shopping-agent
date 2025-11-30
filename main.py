    # 3. VALIDATION
    va = ValidationAgent()
    check = va.validate(plan, preferences, SAMPLE_RECIPES)

    if not check["valid"]:
        print("Plan validation failed:", check["problems"])
        suggestion = check.get("suggestion", {})
        swaps = suggestion.get("swaps", {})
        if swaps:
            print("Applying automatic fixes:", swaps)
            # apply swaps to plan
            for day, new_meal in swaps.items():
                if day in plan:
                    plan[day] = new_meal
            # re-validate
            check2 = va.validate(plan, preferences, SAMPLE_RECIPES)
            if check2["valid"]:
                print("Plan fixed automatically.")
            else:
                print("Still issues after auto-fix:", check2["problems"])
        else:
            print("No automatic fixes available — using fallback planner.")
            plan = mp.plan_week(preferences)
