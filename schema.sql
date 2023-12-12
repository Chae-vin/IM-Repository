CREATE TABLE `budgets` (
  `budget_id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(255) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`budget_id`),
  UNIQUE KEY `category_UNIQUE` (`category`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `transactions` (
  `trans_id` int unsigned NOT NULL AUTO_INCREMENT,
  `budget_id` int DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `trans_date` date NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `last_modified` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `remaining_budget` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`trans_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


CREATE VIEW `get_transactions` AS
    SELECT 
        `t`.`trans_id` AS `trans_id`,
        `b`.`category` AS `category`,
        `t`.`remaining_budget` AS `remaining_budget`,
        `t`.`amount` AS `amount`,
        `t`.`description` AS `description`,
        `t`.`trans_date` AS `trans_date`,
        `t`.`created_at` AS `created_at`
    FROM
        (`transactions` `t`
        LEFT JOIN `budgets` `b` ON ((`t`.`budget_id` = `b`.`budget_id`)))


CREATE DEFINER=`root`@`localhost` PROCEDURE `create_budget`(IN p_category VARCHAR(255), IN p_amount DECIMAL(10, 2))
BEGIN
    INSERT INTO im2.budgets (category, amount) VALUES (p_category, p_amount);
SELECT 
    *
FROM
    im2.budgets
WHERE
    budget_id = LAST_INSERT_ID();
END


CREATE DEFINER=`root`@`localhost` PROCEDURE `create_transaction`(
    IN p_budget_id INT,
    IN p_amount DECIMAL(10, 2),
    IN p_description VARCHAR(255),
    IN p_trans_date DATE
)
BEGIN
    DECLARE remaining_budget DECIMAL(10, 2);

    INSERT INTO im2.transactions(budget_id, amount, description, trans_date) 
    VALUES (p_budget_id, p_amount, p_description, p_trans_date);

    SELECT 
        (b.amount - p_amount)
    INTO remaining_budget
    FROM
        im2.budgets b
    WHERE
        b.budget_id = p_budget_id;

    UPDATE im2.transactions
    SET remaining_budget = remaining_budget
    WHERE trans_id = LAST_INSERT_ID();

    UPDATE im2.budgets
    SET amount = remaining_budget
    WHERE budget_id = p_budget_id;

    SELECT * FROM im2.transactions WHERE trans_id = LAST_INSERT_ID();
END


CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_budget`(IN p_budget_id INT)
BEGIN
    DELETE FROM budgets WHERE budget_id = p_budget_id;
    SELECT p_budget_id AS budget_id;
END



CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_transaction`(IN p_trans_id INT)
BEGIN
    DECLARE rows_deleted INT;

    DELETE FROM im2.transactions WHERE trans_id = p_trans_id;

    SELECT ROW_COUNT() INTO rows_deleted;

    IF rows_deleted > 0 THEN
        SELECT p_trans_id AS trans_id;
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Transaction with the specified ID does not exist';
    END IF;
END




CREATE DEFINER=`root`@`localhost` PROCEDURE `update_budget`(
    IN p_budget_id INT,
    IN p_new_category VARCHAR(255),
    IN p_new_amount DECIMAL(10, 2)
)
BEGIN
    DECLARE category_count INT;

    SELECT COUNT(*) INTO category_count FROM im2.budgets WHERE category = p_new_category;

    IF category_count = 0 OR p_budget_id = (SELECT p_budget_id FROM im2.budgets WHERE category = p_new_category) THEN
        UPDATE im2.budgets SET category = p_new_category, amount = p_new_amount WHERE budget_id = p_budget_id;
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Category must be unique. Another record with the same category already exists.';
    END IF;
    
    SELECT * FROM im2.budgets WHERE budget_id = p_budget_id;
END


CREATE DEFINER=`root`@`localhost` PROCEDURE `update_transaction`(
    IN p_trans_id INT,
    IN p_budget_id INT,
    IN p_amount DECIMAL(10, 2),
    IN p_description VARCHAR(255),
    IN p_trans_date DATE
)
BEGIN
    DECLARE rows_affected INT;

    UPDATE im2.transactions 
    SET
        budget_id = p_budget_id,
        amount = p_amount,
        description = p_description,
        trans_date = p_trans_date
    WHERE trans_id = p_trans_id;

    SELECT ROW_COUNT() INTO rows_affected;

    IF rows_affected > 0 THEN
        SELECT * FROM im2.transactions WHERE trans_id = p_trans_id;
    ELSE
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Transaction with the specified ID does not exist';
    END IF;
END



CREATE DEFINER=`root`@`localhost` TRIGGER `before_transaction_insert` BEFORE INSERT ON `transactions` FOR EACH ROW BEGIN
    DECLARE budget_remaining DECIMAL(10, 2);

     SELECT 
        (b.amount - NEW.amount)
    INTO budget_remaining
    FROM
        im2.budgets b
    WHERE
        b.budget_id = NEW.budget_id;

    IF (SELECT amount FROM im2.budgets WHERE budget_id = NEW.budget_id) <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Budget Violation: Budget is less than or equal to 0';
    END IF;
END


CREATE DEFINER=`root`@`localhost` TRIGGER `update_last_modified` BEFORE UPDATE ON `transactions` FOR EACH ROW BEGIN
    SET NEW.last_modified = CURRENT_TIMESTAMP;
END

CREATE DEFINER=`root`@`localhost` TRIGGER `after_transaction_update` AFTER UPDATE ON `transactions` FOR EACH ROW
BEGIN
    DECLARE new_budget_amount DECIMAL(10, 2);

    SELECT 
        (b.amount - NEW.amount + OLD.amount)
    INTO new_budget_amount
    FROM
        budgets b
    WHERE
        b.budget_id = NEW.budget_id;

    UPDATE budgets
    SET amount = new_budget_amount
    WHERE budget_id = NEW.budget_id;
END;


-- ===================
-- USERS

CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  -- Add other fields as needed
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username_UNIQUE` (`username`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE VIEW `get_users` AS
    SELECT 
        `u`.`user_id` AS `user_id`,
        `u`.`username` AS `username`,
        `u`.`email` AS `email`
    FROM
        `users` `u`;

CREATE DEFINER=`root`@`localhost` PROCEDURE `create_user`(
    IN p_username VARCHAR(255),
    IN p_password VARCHAR(255),
    IN p_email VARCHAR(255)
)
BEGIN
    INSERT INTO users (username, password, email) VALUES (p_username, p_password, p_email);
    SELECT * FROM users WHERE user_id = LAST_INSERT_ID();
END;


CREATE DEFINER=`root`@`localhost` PROCEDURE `update_user`(
    IN p_user_id INT,
    IN p_new_username VARCHAR(255),
    IN p_new_password VARCHAR(255),
    IN p_new_email VARCHAR(255)
)
BEGIN
    UPDATE users
    SET
        username = p_new_username,
        password = p_new_password,
        email = p_new_email
    WHERE user_id = p_user_id;

    SELECT * FROM users WHERE user_id = p_user_id;
END;


CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_user`(IN p_user_id INT)
BEGIN
    DELETE FROM users WHERE user_id = p_user_id;
    SELECT p_user_id AS user_id;
END;

