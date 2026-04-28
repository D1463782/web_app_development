-- ============================================
-- 食譜收藏系統 — SQLite 資料庫建表語法
-- ============================================

-- 啟用外鍵約束（SQLite 預設不啟用）
PRAGMA foreign_keys = ON;

-- -------------------------------------------
-- 食譜表（RECIPES）
-- -------------------------------------------
CREATE TABLE IF NOT EXISTS recipes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    description TEXT    DEFAULT '',
    created_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- -------------------------------------------
-- 材料表（INGREDIENTS）
-- -------------------------------------------
CREATE TABLE IF NOT EXISTS ingredients (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id   INTEGER NOT NULL,
    name        TEXT    NOT NULL,
    quantity    TEXT    DEFAULT '',
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- -------------------------------------------
-- 步驟表（STEPS）
-- -------------------------------------------
CREATE TABLE IF NOT EXISTS steps (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id     INTEGER NOT NULL,
    step_number   INTEGER NOT NULL,
    description   TEXT    NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);
