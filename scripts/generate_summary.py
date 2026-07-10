import json
import sys
import os

def generate_summary(json_path):
    if not os.path.exists(json_path):
        return "Error: File not found."
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    messages = data.get('result', {}).get('threads', [])
    if not messages:
        return "过去 24 小时内没有未读邮件。"
    
    import datetime
    now = datetime.datetime.now(datetime.timezone.utc)
    start_time = now - datetime.timedelta(days=1)
    
    summary_lines = []
    summary_lines.append(f"## 每日未读邮件摘要")
    summary_lines.append(f"报告生成时间：{now.strftime('%Y-%m-%d %H:%M')} (UTC)")
    summary_lines.append(f"覆盖区间：{start_time.strftime('%H:%M')} 至 {now.strftime('%H:%M')}")
    summary_lines.append(f"\n过去 24 小时共有 **{len(messages)} 封未读邮件**。\n---\n")
    
    # Simple classification logic (can be enhanced with LLM later)
    important = []
    newsletter = []
    marketing = []
    
    for thread in messages:
        msg = thread.get('messages', [{}])[0]
        headers = msg.get('pickedHeaders', {})
        subject = headers.get('subject', '无主题')
        sender = headers.get('from', '未知发件人')
        snippet = msg.get('snippet', '')
        
        entry = {
            'sender': sender,
            'subject': subject,
            'snippet': snippet
        }
        
        # Heuristic classification
        low_subject = subject.lower()
        low_sender = sender.lower()
        if any(kw in low_subject or kw in low_sender for kw in ['security', 'alert', 'job', 'match', 'invoice', 'order', 'commande', 'bill', 'urgent', '安全', '职位', '订单', '账单']):
            important.append(entry)
        elif any(kw in low_sender or kw in low_subject for kw in ['substack', 'newsletter', 'news', 'digest', 'valley', 'swyx']):
            newsletter.append(entry)
        else:
            marketing.append(entry)
            
    if important:
        summary_lines.append("### 一、需要留意的邮件\n")
        for e in important:
            summary_lines.append(f"**{e['sender']}**: {e['subject']}\n- {e['snippet']}\n")
            
    if newsletter:
        summary_lines.append("\n### 二、行业资讯与订阅\n")
        for e in newsletter:
            summary_lines.append(f"- **{e['sender']}**: {e['subject']}\n")
            
    if marketing:
        summary_lines.append("\n### 三、其他邮件\n")
        for e in marketing:
            summary_lines.append(f"- {e['sender']}: {e['subject']}\n")
            
    return "\n".join(summary_lines)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(generate_summary(sys.argv[1]))
