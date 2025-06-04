# Metisse 專案協作指南

本文件面向在本倉庫工作的 AI 智能體，旨在說明專案結構、編碼規範、測試執行方式以及 PR 建立規則，協助統一開發流程。

## 專案結構說明

- `metisse/`：核心庫程式碼，包含客戶端實作、工具函式及示例資料等。
- `docs/`：專案文件。
- `pytest_metisse/`：基於 `pytest` 的單元測試。
- `tutorial/`：示例腳本與示例資源，供學習和展示使用。
- 其他檔案：`pyproject.toml` 與 `poetry.lock` 定義了依賴；`Makefile` 提供常用任務；`.github/workflows/` 包含 CI 設定。

## 編碼規範與風格指南

- 程式碼需遵循 [PEP 8](https://peps.python.org/pep-0008/) 以及型別標註規範。
- 本專案使用 [Black](https://github.com/psf/black) 與 [isort](https://github.com/PyCQA/isort) 統一格式化，可透過 `make lint` 執行。
- 請為公共函式和類別撰寫文件字串，保持良好的可讀性。
- Python 版本以 `pyproject.toml` 中定義的 `>=3.8,<3.11` 為準。

## 測試執行方法

1. 安裝依賴：`poetry install`。
2. 本地執行測試：`make local-test`（等同於 `poetry run pytest --cov=metisse -s pytest_metisse`）。
3. 如需在與 CI 相同的 Docker 環境中執行，可使用 `make test`。
4. 程式碼提交前請確保測試全部通過。

## PR 建立規則

- 所有變更應從 `main` 分支建立新分支進行開發，提交後透過 Pull Request 合併。
- 提交前必須執行 `make lint` 與測試，確保格式及測試無誤。
- PR 標題需簡潔明瞭，內文應描述主要變更及相關 issue（如有）。
- CI 會自動執行測試與覆蓋率檢查，若失敗請修復後再重新提交。

## 開發流程說明

1. 複製倉庫並切換到新分支。
2. 執行 `poetry install` 安裝依賴。
3. 編碼時遵循以上風格指南，並適時撰寫或更新測試。
4. 使用 `make lint` 格式化程式碼，使用 `make local-test` 執行測試。
5. 提交並推送變更，隨後建立 PR 等待程式碼審查與合併。

