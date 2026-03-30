-- Procedure: insert or update user
CREATE OR REPLACE PROCEDURE insert_or_update_user(
    p_username VARCHAR,
    p_phone VARCHAR
)
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE username = p_username) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE username = p_username;
    ELSE
        INSERT INTO phonebook(username, phone)
        VALUES (p_username, p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Procedure: insert many users
CREATE OR REPLACE PROCEDURE insert_many_users(
    IN p_usernames TEXT[],
    IN p_phones TEXT[]
)
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_length(p_usernames, 1) LOOP
        IF p_phones[i] ~ '^[0-9+\-() ]{6,20}$' THEN
            CALL insert_or_update_user(
                p_usernames[i],
                p_phones[i]
            );
        ELSE
            RAISE NOTICE 'Incorrect data: %, %', p_usernames[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Procedure: delete by username or phone
CREATE OR REPLACE PROCEDURE delete_user(p_value VARCHAR)
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE username = p_value
       OR phone = p_value;
END;
$$ LANGUAGE plpgsql;