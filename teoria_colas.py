class QueuePriorityModel:
    def __init__(self, mu: float, lambdas: list[float]):

        self.mu = mu
        self.lambdas = lambdas
        self.k = len(lambdas)
        self.lambda_total = sum(lambdas)
        self.rhos = [l / mu for l in lambdas]
        self.rho_total = sum(self.rhos)

    def is_stable(self) -> bool:
        return self.rho_total < 1.0

    def calculate_fifo_wq(self) -> float:
        return self.lambda_total / (self.mu * (self.mu - self.lambda_total))

    def calculate_non_preemptive_wq(self) -> list[float]:
        w0 = self.lambda_total / (2 * (self.mu ** 2))
        wq_list = []

        sigma_prev = 0.0
        for rho_i in self.rhos:
            sigma_curr = sigma_prev + rho_i
            wq_i = w0 / ((1 - sigma_prev) * (1 - sigma_curr))
            wq_list.append(wq_i)
            sigma_prev = sigma_curr

        return wq_list

    def print_challenge_results(self):
        print("REto de triaje hospitalario")
        
        if not self.is_stable():
            print("ERROR: El sistema es inestable")
            return

        print(f" Tasa de servicio (mu): {self.mu} pacientes/hora")
        print(f" Ocupación Total (rho): {self.rho_total * 100:.2f}% (Sistema Estable)")
        print("-" * 65)

        wq_fifo_hrs = self.calculate_fifo_wq()
        wq_fifo_min = wq_fifo_hrs * 60
        print(f"Tiempo de espera en Cola FIFO: {wq_fifo_min:.2f} min\n")

        wq_np_hrs = self.calculate_non_preemptive_wq()
        
        print(f"{'Clase / Categoria':<25} | {'Wq (min)':<10} | {'Comparaciopn vs FIFO':<25}")
        
        for i, wq_hrs in enumerate(wq_np_hrs):
            wq_min = wq_hrs * 60
            diff_min = wq_fifo_min - wq_min
            
            if diff_min > 0:
                pct = (diff_min / wq_fifo_min) * 100
                comparacion = f"Gana {diff_min:.2f} min ({pct:.1f}% más rápido)"
            else:
                pct = (abs(diff_min) / wq_fifo_min) * 100
                comparacion = f"Pierde {abs(diff_min):.2f} min ({pct:.1f}% más espera)"

            print(f"Clase {i+1} (Prioridad {i+1}): {wq_min:8.2f} min | {comparacion}")

if __name__ == "__main__":
    
    tasas_llegada = [1.0, 2.0, 3.0]
    tasa_servicio = 10.0
    modelo_hospital = QueuePriorityModel(mu=tasa_servicio, lambdas=tasas_llegada)
    modelo_hospital.print_challenge_results()
