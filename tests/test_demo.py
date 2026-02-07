import pytest
from dirty_equals import IsInt, IsUUID
from inline_snapshot import snapshot


def get_user_data():
    """模拟一个返回复杂数据的函数"""
    return {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "age": 25,
        "name": "Astral Developer",
        "tags": ["python", "uv", "fast"],
    }


def test_user_data_with_dirty_equals():
    data = get_user_data()
    # 使用 dirty-equals 进行声明式断言
    assert data == {
        "id": IsUUID(4),  # 校验是否为 UUID v4 格式
        "age": IsInt(gt=20),  # 校验是否为大于 20 的整数
        "name": "Astral Developer",
        "tags": ["python", "uv", "fast"],
    }


def test_with_inline_snapshot():
    data = get_user_data()
    # 第一次运行时，snapshot() 会自动填充内容
    # 以后如果数据变了，你可以运行 `uv run pytest --inline-snapshot=fix` 自动更新代码
    assert data == snapshot({'id':'550e8400-e29b-41d4-a716-446655440000','age':25 ,'name':'Astral Developer','tags':['python','uv','fast']})


@pytest.mark.asyncio
async def test_async_demo():
    """演示异步测试"""
    import asyncio

    await asyncio.sleep(0.1)
    assert True
