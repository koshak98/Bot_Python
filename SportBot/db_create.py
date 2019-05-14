import sqlite3

create_scripts = [
                  '''
                      CREATE TABLE club (
                      club_id INT PRIMARY KEY
                      , club_nm VARCHAR UNIQUE
                      , club_url VARCHAR
                      );
                      ''',
                  '''
                      CREATE TABLE user (
                      user_id INT PRIMARY KEY
                      , user_nm VARCHAR
                      , favourite_club_id INT
                      , FOREIGN KEY (favourite_club_id) REFERENCES club(club_id)
                      );
                      '''
                  ]

insert_club_script = '''
    INSERT
    INTO club (club_id, club_nm, club_url)
    VALUES (?, ?, ?)
    ;
    '''

insert_user_script = '''
    INSERT
    INTO user(user_id, user_nm, favourite_club_id)
    VALUES(?, ?, ?)
    ;
    '''

clubs = [
         [1, 'Real Madrid', 'https://www.realmadrid.com/en'],
         [2, 'Barcelona', 'https://www.fcbarcelona.com/en/'],
         [3, 'Manchester United', 'https://www.manutd.com'],
         [4, 'Manchester City', 'https://www.mancity.com'],
         [5, 'Chelsea', 'https://www.chelseafc.com/en'],
         [6, 'Bayern', 'https://fcbayern.com/ru']
         ]

with sqlite3.connect('clubs.db') as conn:
    cur = conn.cursor()
    for statement in create_scripts:
        cur.execute(statement)
    conn.commit()
    for club_info in clubs:
        cur.execute(insert_club_script, club_info)
    conn.commit()
    cur.execute(insert_user_script, [0, 'Bot', '1'])
    conn.commit()
    print(cur.execute('SELECT * FROM club;').fetchall())
