# Blockchain Structure



#### blockchain 定义

1. 初始函数  __init__(self)
   - chain 当前链的列表
   - current_transactions 记录当前区块的交易
   - nodes 记录当前区块链的临节点，临界点可以在同一条合法链上继续挖矿并交易
2.  注册临节点 register_node(self, address)
   - 将地址加入到当前blockchain的nodes中
3. 验证POW， valid_proof(last_proof, proof)
   - 将前一个block的proof和当前block的proof合并取hash
   - 验证是否满足要求，返回boolean值 
4. POW算法proof_of_work(self, proof)
   - 从0开始试验，直到找到合适的值
5. 取block的hash hash(block)
6. 取上一个block last_block(self)
7. 给block添加信息 new_transaction(self, sender, recipient, amount)
   - 在当前区块的current_transactions中append新的内容
   - 返回记录次信息的block index
8. 新block new_block(self, proof, previous_hash=None)
   - block结构
     - index
     - timestamp
     - transactions
     - proof
     - previous_hash
   - 清空self.current_transactions
   - 将新的block加入链中
9. 确认当前链是最长合法链
   - 从最开始的一个block开始验证
     - 验证previous_hash == hash(last_block)
     - 验证valid_proof(proof, last_block[proof])
   - 验证通过之后迭代验证下一个block，直到最后一个block
10. 切换到最长合法链
    - 遍历所有nodes
      - 如果长度比当前链长
      - 如果新的链合法
      - 将self.chain 切换为最长合法链



#### 应用

1. 挖矿
2. 新的transactions
3. 获取当前链
4. 注册新的nodes
5. 是否切换为最长链

