-- TRANSACTIONS:
ALTER TABLE
  TRANSACTIONS DROP CONSTRAINT IF EXISTS FK_TRANSACTIONS_CATEGORIES;


ALTER TABLE
  TRANSACTIONS
ADD
  CONSTRAINT FK_TRANSACTIONS_CATEGORIES FOREIGN KEY (CATEGORY_ID) REFERENCES TRANSACTIONS (ID);
