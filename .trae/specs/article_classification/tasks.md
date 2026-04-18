# 文章分类词提取功能 - The Implementation Plan (Decomposed and Prioritized Task List)

## [x] Task 1: 分析网页结构，定位分类词位置
- **Priority**: P0
- **Depends On**: None
- **Description**: 
  - 访问并分析多个公告详情页，寻找分类词的HTML位置
  - 检查列表页和详情页的结构差异
  - 收集常见的分类词示例
- **Acceptance Criteria Addressed**: AC-1
- **Test Requirements**:
  - `programmatic` TR-1.1: 访问至少5个不同公告页面 ✓
  - `human-judgement` TR-1.2: 记录分类词可能的HTML位置和样式 ✓
- **Notes**: 已完成！分类词位置：1)列表页<span class="wjj">；2)详情页meta keywords
发现16个分类词：全部,文件公告,学术报告,招标信息,会议通知,党政事务,组织人事,科研信息,招生就业,教学考试,创新创业,学术研讨,专题讲座,校园活动,学院动态,其他

## [x] Task 2: 实现分类词提取函数
- **Priority**: P0
- **Depends On**: Task 1
- **Description**: 
  - 在 `parser.py` 中添加 `extract_category()` 函数
  - 实现从HTML中提取分类词的逻辑
  - 处理分类词的清洗和标准化
- **Acceptance Criteria Addressed**: AC-1, AC-4
- **Test Requirements**:
  - `programmatic` TR-2.1: 测试至少3种不同分类词的提取 ✓
  - `programmatic` TR-2.2: 测试无分类词的情况，返回空字符串 ✓
  - `human-judgement` TR-2.3: 代码可读性检查，有清晰的注释 ✓

## [x] Task 3: 修改详情解析函数，返回分类词
- **Priority**: P0
- **Depends On**: Task 2
- **Description**: 
  - 修改 `parse_announcement_detail()` 函数
  - 在返回结果中添加 `'category': ''` 字段
  - 调用 `extract_category()` 获取分类词
- **Acceptance Criteria Addressed**: AC-1, AC-4
- **Test Requirements**:
  - `programmatic` TR-3.1: 验证返回的字典包含 `category` 字段 ✓
  - `programmatic` TR-3.2: 验证有分类词的情况能正确提取 ✓
  - `programmatic` TR-3.3: 验证无分类词的情况返回空字符串 ✓

## [x] Task 4: 修改文件保存函数，添加分类词前缀
- **Priority**: P0
- **Depends On**: Task 3
- **Description**: 
  - 修改 `save_announcement()` 函数
  - 检查 `detail['category']` 是否有值
  - 如果有，添加到标题前缀
  - 使用适当的分隔符（建议使用"【分类】"格式）
- **Acceptance Criteria Addressed**: AC-2, AC-3, AC-4
- **Test Requirements**:
  - `programmatic` TR-4.1: 验证有分类词的文件名格式为 `YYYY-MM-DD_【分类】标题.md` ✓
  - `programmatic` TR-4.2: 验证无分类词的文件名保持原格式 ✓
  - `human-judgement` TR-4.3: 验证文件名可读性好，分隔符清晰 ✓

## [x] Task 5: 更新公告数据结构，传递分类词
- **Priority**: P1
- **Depends On**: Task 3
- **Description**: 
  - 在 `parse_announcement_list()` 返回的字典中添加 `category` 字段
  - 在 `main.py` 中更新公告数据，使用详情页的分类词
  - 确保分类词在整个流程中正确传递
- **Acceptance Criteria Addressed**: AC-2
- **Test Requirements**:
  - `programmatic` TR-5.1: 验证列表页返回的字典包含 `category` 字段 ✓
  - `programmatic` TR-5.2: 验证详情页分类词能更新到公告数据中 ✓
  - `programmatic` TR-5.3: 验证摘要生成时分类词信息可用 ✓

## [x] Task 6: 集成测试，验证完整流程
- **Priority**: P0
- **Depends On**: Task 4, Task 5
- **Description**: 
  - 运行完整的爬虫流程
  - 测试多种类型的公告
  - 验证所有功能正常工作
- **Acceptance Criteria Addressed**: AC-1, AC-2, AC-3, AC-4, AC-5
- **Test Requirements**:
  - `programmatic` TR-6.1: 验证完整爬虫能正常运行 ✓
  - `programmatic` TR-6.2: 验证有分类词的文件命名正确 ✓
  - `programmatic` TR-6.3: 验证无分类词的文件命名正确 ✓
  - `human-judgement` TR-6.4: 验证所有现有功能不受影响 ✓

## [x] Task 7: 文档更新，记录功能使用
- **Priority**: P2
- **Depends On**: Task 6
- **Description**: 
  - 更新 README.md，说明分类词功能
  - 记录分类词的提取逻辑
  - 添加使用示例
- **Acceptance Criteria Addressed**: AC-5
- **Test Requirements**:
  - `human-judgement` TR-7.1: README文档清晰易懂 ✓
  - `human-judgement` TR-7.2: 有功能说明和使用示例 ✓
- **Acceptance Criteria Addressed**: AC-1, AC-4
- **Test Requirements**:
  - `programmatic` TR-2.1: 测试至少3种不同分类词的提取
  - `programmatic` TR-2.2: 测试无分类词的情况，返回空字符串
  - `human-judgement` TR-2.3: 代码可读性检查，有清晰的注释

## [ ] Task 3: 修改详情解析函数，返回分类词
- **Priority**: P0
- **Depends On**: Task 2
- **Description**: 
  - 修改 `parse_announcement_detail()` 函数
  - 在返回结果中添加 `'category': ''` 字段
  - 调用 `extract_category()` 获取分类词
- **Acceptance Criteria Addressed**: AC-1, AC-4
- **Test Requirements**:
  - `programmatic` TR-3.1: 验证返回的字典包含 `category` 字段
  - `programmatic` TR-3.2: 验证有分类词的情况能正确提取
  - `programmatic` TR-3.3: 验证无分类词的情况返回空字符串

## [ ] Task 4: 修改文件保存函数，添加分类词前缀
- **Priority**: P0
- **Depends On**: Task 3
- **Description**: 
  - 修改 `save_announcement()` 函数
  - 检查 `detail['category']` 是否有值
  - 如果有，添加到标题前缀
  - 使用适当的分隔符（建议使用"【分类】"格式）
- **Acceptance Criteria Addressed**: AC-2, AC-3, AC-4
- **Test Requirements**:
  - `programmatic` TR-4.1: 验证有分类词的文件名格式为 `YYYY-MM-DD_【分类】标题.md`
  - `programmatic` TR-4.2: 验证无分类词的文件名保持原格式
  - `human-judgement` TR-4.3: 验证文件名可读性好，分隔符清晰

## [ ] Task 5: 更新公告数据结构，传递分类词
- **Priority**: P1
- **Depends On**: Task 3
- **Description**: 
  - 在 `parse_announcement_list()` 返回的字典中添加 `category` 字段
  - 在 `main.py` 中更新公告数据，使用详情页的分类词
  - 确保分类词在整个流程中正确传递
- **Acceptance Criteria Addressed**: AC-2
- **Test Requirements**:
  - `programmatic` TR-5.1: 验证列表页返回的字典包含 `category` 字段
  - `programmatic` TR-5.2: 验证详情页分类词能更新到公告数据中
  - `programmatic` TR-5.3: 验证摘要生成时分类词信息可用

## [ ] Task 6: 集成测试，验证完整流程
- **Priority**: P0
- **Depends On**: Task 4, Task 5
- **Description**: 
  - 运行完整的爬虫流程
  - 测试多种类型的公告
  - 验证所有功能正常工作
- **Acceptance Criteria Addressed**: AC-1, AC-2, AC-3, AC-4, AC-5
- **Test Requirements**:
  - `programmatic` TR-6.1: 验证完整爬虫能正常运行
  - `programmatic` TR-6.2: 验证有分类词的文件命名正确
  - `programmatic` TR-6.3: 验证无分类词的文件命名正确
  - `human-judgement` TR-6.4: 验证所有现有功能不受影响

## [ ] Task 7: 文档更新，记录功能使用
- **Priority**: P2
- **Depends On**: Task 6
- **Description**: 
  - 更新 README.md，说明分类词功能
  - 记录分类词的提取逻辑
  - 添加使用示例
- **Acceptance Criteria Addressed**: AC-5
- **Test Requirements**:
  - `human-judgement` TR-7.1: README文档清晰易懂
  - `human-judgement` TR-7.2: 有功能说明和使用示例
