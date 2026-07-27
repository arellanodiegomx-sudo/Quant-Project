from dataclasses import dataclass

@dataclass
class RiskManager:
    max_position_pct: float = 0.20
    stop_loss_pct: float = 0.10
    max_drawdown_pct: float = 0.15

    def position_size(self, cash: float, price: float) -> int:
        max_spend = cash * self.max_position_pct
        return int(max_spend // price)
    
    def should_stop_loss(self, buy_price: float, current_price: float) -> bool:
        loss_pct = (buy_price - current_price) / buy_price
        return loss_pct >= self.stop_loss_pct
    
    def should_halt(self, peak_value: float, current_value: float) -> bool:
        drawdown = (peak_value - current_value) / peak_value
        return drawdown>= self.max_drawdown_pct