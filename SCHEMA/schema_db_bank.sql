DROP DATABASE IF EXISTS BancoDB;
CREATE DATABASE BancoDB;
USE BancoDB;

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    gmail VARCHAR(55) UNIQUE NOT NULL,
    phone VARCHAR(15),
    kyc_status ENUM("ACTIVE", "INACTIVE") DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE user_device (
    id_device INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    device_type VARCHAR(45) NOT NULL,
    os VARCHAR(45) NOT NULL,
    last_login_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE currencies (
    currency_id INT AUTO_INCREMENT PRIMARY KEY UNIQUE,
    c_code VARCHAR(15) NOT NULL UNIQUE,
    c_name VARCHAR(100) NOT NULL,
    is_crypto BOOLEAN NOT NULL DEFAULT FALSE
) ENGINE=InnoDB;

CREATE TABLE accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    currency_id INT NOT NULL,
    account_type ENUM('SAVINGS','CHECKING','CREDIT'),
    a_status ENUM("ACTIVE", "INACTIVE") DEFAULT 'ACTIVE',
    create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (currency_id) REFERENCES currencies(currency_id) ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE account_balances(
    account_id INT PRIMARY KEY,
    current_balance DECIMAL(15,2) NOT NULL,
    last_update_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE transactions_types (
    transaction_type_id  INT AUTO_INCREMENT PRIMARY KEY,
    t_name VARCHAR(30) NOT NULL UNIQUE,
    t_description VARCHAR(250)
) ENGINE = InnoDB;

CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL,
    transaction_type_id INT NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    currency_id INT NOT NULL,
    t_status   ENUM('PENDING','COMPLETED','FAILED','REVERSED') DEFAULT 'PENDING',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE RESTRICT,
    FOREIGN KEY (transaction_type_id) REFERENCES transactions_types(transaction_type_id) ON DELETE RESTRICT,
    FOREIGN KEY (currency_id) REFERENCES currencies (currency_id) ON DELETE RESTRICT
) ENGINE = InnoDB;

CREATE TABLE audit_log(
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    entity_name VARCHAR(100) NOT NULL,
    entity_id INT NOT NULL,
    action VARCHAR(50) NOT NULL,
    performed_by INT NOT NULL,
    performed_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    old_value TEXT,
    new_value TEXT
) ENGINE = InnoDB;

CREATE TABLE transactions_raw (
    raw_id INT AUTO_INCREMENT PRIMARY KEY,
    raw_data TEXT,
    insert_at  DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

CREATE TABLE accounts_raw (
    raw_id INT AUTO_INCREMENT PRIMARY KEY,
    raw_data TEXT,
    insert_at  DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

CREATE TABLE daily_account_snapshots (
    account_id INT NOT NULL,
    snapshot_date DATE NOT NULL,
    closing_balance DECIMAL(15,2) NOT NULL,
    PRIMARY KEY(account_id ,snapshot_date )
) ENGINE = InnoDB;

CREATE TABLE  user_monthly_metrics(
    user_id INT NOT NULL,
    u_year_month CHAR(7) NOT NULL,
    total_transactions INT NOT NULL,
    total_volume DECIMAL(15,2) NOT NULL,
    avg_transaction DECIMAL(15,2) NOT NULL,
    PRIMARY KEY(user_id, u_year_month)
)ENGINE = InnoDB;
