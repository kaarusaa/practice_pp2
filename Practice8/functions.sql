-- Function to search contacts by pattern
CREATE OR REPLACE FUNCTION search_contacts(search_pattern TEXT)
RETURNS TABLE (
    username VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.username, p.phone
    FROM phonebook p
    WHERE p.username ILIKE '%' || search_pattern || '%'
       OR p.phone ILIKE '%' || search_pattern || '%'
    ORDER BY p.id;
END;
$$ LANGUAGE plpgsql;

-- Function for pagination
CREATE OR REPLACE FUNCTION get_contacts_paginated(limit_count INT, offset_count INT)
RETURNS TABLE (
    id INT,
    username VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.username, p.phone
    FROM phonebook p
    ORDER BY p.id
    LIMIT limit_count OFFSET offset_count;
END;
$$ LANGUAGE plpgsql;