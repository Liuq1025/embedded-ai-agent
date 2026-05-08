import time
import traceback # 引入报错追踪模块

# ==========================================
# 1. 定义系统状态与数据结构
# ==========================================
class AgentState:
    def __init__(self, task_requirement):
        self.task_requirement = task_requirement  
        self.datasheet_context = ""               
        self.generated_code = ""                  
        self.test_logs = ""                       
        self.error_count = 0                      
        self.max_retries = 3                      
        self.status = "INIT"                      

# ==========================================
# 2. 定义多智能体 (Multi-Agents)
# ==========================================
class DocumentParsingAgent:
    def run(self, state: AgentState) -> AgentState:
        print("[Agent 1] 📄 正在解析 Datasheet 及寄存器映射表...")
        time.sleep(1) 
        
        mock_context = """
        Register: PWR_CR (Power control register)
        Bit 1: PDDS (Power down deepsleep) - Set to 1 to enter Standby mode.
        Bit 8: DBP (Disable backup domain write protection) - Set to 1 to enable.
        """
        state.datasheet_context = mock_context
        state.status = "DOCS_PARSED"
        print("  -> 解析完成：已提取 PWR_CR 寄存器配置规则。\n")
        return state

class CodingAgent:
    def run(self, state: AgentState) -> AgentState:
        print("[Agent 2] 💻 正在结合上下文进行长链推理与代码生成...")
        time.sleep(1.5) 
        
        if state.error_count == 0:
            mock_code = """
void enter_standby_mode(void) {
    // Enable DBP
    PWR->CR |= (1 << 8); 
    // Set PDDS bit
    PWR->CR |= (1 << 1); 
    // Enter deepsleep (Bug: missed SCB->SCR configuration)
    __WFI(); 
}"""
        else:
            print(f"  -> 触发反思机制！根据报错日志 [{state.test_logs}] 修正代码...")
            mock_code = """
void enter_standby_mode(void) {
    PWR->CR |= (1 << 8); 
    PWR->CR |= (1 << 1); 
    SCB->SCR |= SCB_SCR_SLEEPDEEP_Msk; // Fixed: Added SLEEPDEEP config
    __WFI(); 
}"""
            
        state.generated_code = mock_code
        state.status = "CODE_GENERATED"
        print("  -> 代码生成完毕。\n")
        return state

class TestingAgent:
    def run(self, state: AgentState) -> AgentState:
        print("[Agent 3] 🛠️ 正在进行自动化编译与 HIL 模拟测试...")
        time.sleep(1)
        
        if "SCB_SCR_SLEEPDEEP_Msk" not in state.generated_code:
            state.test_logs = "Error: Did not enter deep sleep. SCB_SCR_SLEEPDEEP register not set."
            state.status = "TEST_FAILED"
            state.error_count += 1
            print(f"  -> ❌ 测试失败 (第 {state.error_count} 次): 捕获到寄存器漏配错误。\n")
        else:
            state.test_logs = "Success: Power consumption dropped to Standby target range."
            state.status = "TEST_PASSED"
            print("  -> ✅ 测试通过！逻辑闭环完成。\n")
            
        return state

# ==========================================
# 3. 核心逻辑流引擎 (Workflow Engine)
# ==========================================
class AgenticWorkflow:
    def __init__(self):
        self.doc_agent = DocumentParsingAgent()
        self.coder_agent = CodingAgent()
        self.test_agent = TestingAgent()
        
    def execute(self, task_requirement: str):
        print(f"=== 🚀 启动嵌入式代码生成 Agent ===")
        print(f"目标任务: {task_requirement}\n")
        
        state = AgentState(task_requirement)
        state = self.doc_agent.run(state)
        
        while state.status != "TEST_PASSED" and state.error_count < state.max_retries:
            state = self.coder_agent.run(state)
            state = self.test_agent.run(state)
            
            if state.status == "TEST_FAILED":
                print("⚠️ 启动 Self-Reflection (自我反思) 流程...")
        
        if state.status == "TEST_PASSED":
            print("=== 🎉 最终输出通过验证的 C 代码 ===")
            print(state.generated_code)
        else:
            print("=== 🛑 达到最大迭代次数，任务失败。请人工介入。===")

# ==========================================
# 4. 运行入口 (加入了防闪退保护罩)
# ==========================================
if __name__ == "__main__":
    try:
        # 尝试执行核心业务逻辑
        workflow = AgenticWorkflow()
        workflow.execute("配置 STM32G4 芯片进入 Standby 低功耗模式，并通过 WFI 指令休眠")
    except Exception as e:
        # 如果中间有任何报错，拦截错误并打印出来，防止窗口闪退
        print("\n" + "="*40)
        print("❌ 糟糕，程序运行中出现报错了！错误信息如下：")
        traceback.print_exc()
        print("="*40 + "\n")
    finally:
        # 无论成功还是失败，最后一定执行这一句，按住窗口
        input("\n程序运行结束，请按回车键 (Enter) 退出窗口...")