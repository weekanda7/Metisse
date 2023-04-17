# metisse 套件說明文件

metisse 是一個用於自動化圖像識別和操作任務的 Python 庫。它提供了一組用戶友好的方法，讓用戶能夠使用圖像識別技術執行自動點擊、滑動和按壓操作。以下是 metisse 主要功能和用法的簡要概述：

## MetisseClass

MetisseClass 是 metisse 中包含所有基本圖像識別和操作方法的主要類。要使用 metisse，您需要創建一個繼承自 MetisseClass 的子類並根据需要實現自定義方法。

### 方法：

- `check_image_recognition()`：檢查圖像識別結果。
- `default_tap()`：在識別到的圖像上執行點擊操作。
- `default_swipe()`：在識別到的圖像上執行滑動操作。
- `default_press()`：在識別到的圖像上執行按壓操作。
- `save_screenshot_compression()`：保存壓縮後的屏幕截圖。
- `crop_screenshot()`：裁剪並保存屏幕截圖。
- `execute_time_sleep()`：等待指定的時間。

## ImageRecognitionParams

ImageRecognitionParams 是一個用於配置圖像識別參數的 dataclass。用戶可以根据需要自定義此類以在 metisse 方法中使用。

### 參數：

- `template_image_name`：模板圖像的名稱。
- `compare_times_counter`：圖像識別比較次數。
- `screenshot_wait_time`：截取屏幕截圖之間的等待時間（以秒為單位）。
- `accuracy_val`：圖像識別的準確度值。
- `is_refresh_screenshot`：是否刷新屏幕截圖。
- `screen_image_name`：屏幕圖像的名稱。
- `screen_image_primary_dir`：屏幕圖像的主目錄。
- `screen_image_secondary_dir`：屏幕圖像的次目錄。
- `screen_image_subdirs`：屏幕圖像的第三層或更高子目錄列表。
- `template_image_primary_dir`：模板圖像的主目錄。
- `template_image_secondary_dir`：模板圖像的次目錄。
- `template_image_subdirs`：模板圖像的第三層或更高子目錄列表。
- `is_backup`：是否創建識別圖像的備份。
- `repeatedly_screenshot_times`：重複截屏次數。

## SaveParams

SaveParams 是一個用於配置保存參數的 dataclass。用戶可以根据需要自定義此類以在 metisse 方法中使用。

## 參數

- `load_image_primary_dir`：加載圖像的主目錄。
- `save_image_primary_dir`：保存圖像的主目錄。
- `save_image_name`：保存的圖像名稱。
- `screenshot_wait_time`：截取屏幕截圖之間的等待時間（以秒為單位）。
- `compression`：保存圖像的壓縮比率。
- `load_image_name`：要加載的圖像名稱。
- `save_image_secondary_dir`：保存圖像的次目錄。
- `save_image_subdirs`：保存圖像的第三層或更高子目錄列表。
- `load_image_secondary_dir`：加載圖像的次目錄。
- `load_image_subdirs`：加載圖像的第三層或更高子目錄列表。
- `is_save_image_name_add_time`：是否在保存的圖像名稱中附加當前時間。
- `is_refresh_screenshot`：是否刷新屏幕截圖。

## DeviceParams

DeviceParams 是一個包含與 metisse 運行設備相關的參數的 dataclass。這些參數可用於根據設備的規格自定義庫的行為。

### 參數

- `device_id`：表示設備唯一標識符的字符串。
- `os_environment`：表示設備操作系統環境的字符串（例如：“Android”，“Ios”）。

## UiClientParams

UiClientParams 是一個包含與 metisse 庫用戶界面相關的參數的 dataclass。這些參數可用於自定義在 metisse 中使用的用戶界面元素的外觀和行為。

### 參數

- `image_label`：用於在用戶界面中顯示圖像的 QLabel 對象。
- `log_label`：用於在用戶界面中顯示日誌消息的 QLabel 對象。

## ImageRecognitionResult

ImageRecognitionResult 是一個包含圖像識別結果相關信息的類。此類可用於存儲和管理由 metisse 執行的圖像識別操作的結果。

### 屬性

- `is_recognized`：表示圖像識別是否成功的布爾值。
- `coordinate`：包含識別圖像的 x 和 y 坐標的元組（例如：（x，y））。
- `coordinates_list`：包含所有識別圖像的 x 和 y 坐標的元組列表。
- `recognition_threshold`：表示圖像識別過程中使用的識別閾值的浮點值。

## 使用 metisse 的典型步驟

1. 創建一個繼承自 MetisseClass 的子類。
2. 按需要自定義 ImageRecognitionParams 和 SaveParams dataclass。
3. 在子類中實現所需的圖像識別和操作方法。
4. 創建子類的實例並調用相應的方法以執行腳本。

請參考提供的使用示例以了解如何在實際項目中使用 metisse。