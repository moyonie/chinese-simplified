// DayJS 中文配置
dayjs.locale('zh-cn');

// 自定义配置
dayjs.updateLocale('zh-cn', {
  // 周起始日：周一（中国标准）
  weekStart: 1,
  
  // 序数格式
  ordinal: (number, period) => {
    switch (period) {
      case 'D':
      case 'd':
        return number + '日';
      default:
        return number + '号';
    }
  },
  
  months: [
    '一月', '二月', '三月', '四月', '五月', '六月',
    '七月', '八月', '九月', '十月', '十一月', '十二月'
  ],
  monthsShort: [
    '1 月', '2 月', '3 月', '4 月', '5 月', '6 月',
    '7 月', '8 月', '9 月', '10 月', '11 月', '12 月'
  ],
  weekdays: [
    '星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'
  ],
  weekdaysShort: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'],
  weekdaysMin: ['日', '一', '二', '三', '四', '五', '六'],
  relativeTime: {
    future: '%s后',
    past: '%s前',
    s: '几秒',
    m: '1 分钟',
    mm: '%d 分钟',
    h: '1 小时',
    hh: '%d 小时',
    d: '1 天',
    dd: '%d 天',
    M: '1 个月',
    MM: '%d 个月',
    y: '1 年',
    yy: '%d 年'
  }
});
