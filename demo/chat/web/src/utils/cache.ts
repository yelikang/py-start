/**
 * localStorage 本地化存储工具类
 */
class LocalStorageCache {
  /**
   * 存储数据到 localStorage
   * @param key 存储的键名
   * @param value 要存储的值
   */
  static set(key: string, value: any): void {
    try {
      const serializedValue = JSON.stringify(value);
      localStorage.setItem(key, serializedValue);
    } catch (error) {
      console.error('存储数据到 localStorage 失败:', error);
    }
  }

  /**
   * 从 localStorage 读取数据
   * @param key 存储的键名
   * @param defaultValue 默认值，当键不存在或解析失败时返回
   * @returns 存储的值或默认值
   */
  static get<T = any>(key: string, defaultValue: T): T {
    try {
      const item = localStorage.getItem(key);
      if (item === null) {
        return defaultValue;
      }
      return JSON.parse(item);
    } catch (error) {
      console.error('从 localStorage 读取数据失败:', error);
      return defaultValue;
    }
  }

  /**
   * 删除指定的 localStorage 项
   * @param key 要删除的键名
   */
  static remove(key: string): void {
    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.error('删除 localStorage 项失败:', error);
    }
  }

  /**
   * 清除所有 localStorage 数据
   */
  static clear(): void {
    try {
      localStorage.clear();
    } catch (error) {
      console.error('清除 localStorage 失败:', error);
    }
  }

  /**
   * 检查指定的键是否存在
   * @param key 要检查的键名
   * @returns 是否存在
   */
  static has(key: string): boolean {
    try {
      return localStorage.getItem(key) !== null;
    } catch (error) {
      console.error('检查 localStorage 键存在性失败:', error);
      return false;
    }
  }

  /**
   * 获取所有 localStorage 键名
   * @returns 键名数组
   */
  static keys(): string[] {
    try {
      return Object.keys(localStorage);
    } catch (error) {
      console.error('获取 localStorage 键名失败:', error);
      return [];
    }
  }

  /**
   * 获取 localStorage 已使用的存储大小（字节）
   * @returns 已使用的字节数
   */
  static getSize(): number {
    try {
      let size = 0;
      for (let key in localStorage) {
        if (localStorage.hasOwnProperty(key)) {
          size += localStorage[key].length + key.length;
        }
      }
      return size;
    } catch (error) {
      console.error('获取 localStorage 大小失败:', error);
      return 0;
    }
  }
}

// 导出默认实例和类
// export default LocalStorageCache;

// 导出便捷方法
export const cache = {
  set: LocalStorageCache.set,
  get: LocalStorageCache.get,
  remove: LocalStorageCache.remove,
  clear: LocalStorageCache.clear,
  has: LocalStorageCache.has,
};
