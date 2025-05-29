def calculate_fake_score(profile):
    score = 0

    # 1. Profil fotoğrafı var mı?
    if not profile.profile_pic_url:
        score += 30

    # 2. Biyografisi var mı, varsa ne kadar uzun?
    bio = profile.biography.strip() if profile.biography else ""
    if len(bio) == 0:
        score += 25
    elif len(bio) < 10:
        score += 15

    # 3. Gönderisi var mı, varsa kaç tane?
    if profile.mediacount == 0:
        score += 30
    elif profile.mediacount <= 3:
        score += 15

    # 4. Gizli hesap mı?
    if profile.is_private:
        score += 10

    # 5. Onaylı hesap mı?
    if profile.is_verified:
        score -= 20

    # 6. Takipçi / Takip edilen oranı
    followers = profile.followers
    followees = profile.followees

    if followees == 0:
        score += 20
    else:
        ratio = followers / followees
        if ratio < 0.3:
            score += 20
        elif ratio > 6:
            score -= 10

    return max(0, min(100, score))
