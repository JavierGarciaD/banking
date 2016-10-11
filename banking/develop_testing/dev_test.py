

import credit
import interest_rates









if __name__ == '__main__':
    proyeccion = 36
    producto = 'Vehiculos'
    plazo = 36
    tasas = interest_rates.models.InterestRateModel.fixed(plazo, 0.0145)
    prepago = credit.prepayment.PrepaymentModel.zero(plazo)
    modelo_credito = credit.constructor.CreditModel.simple(plazo)
    presupuesto = [70000] * proyeccion
    
    
    cont_conditions = dict(balance = 0.0,
                           ppmt = [0.0 / plazo] * plazo,
                           fixed_rate = [0.012] * plazo,
                           spread_DTF = None,
                           spread_IBR = None,
                           repricing = None)



    cosecha_contractual = credit.constructor.contractual_vintage(cont_conditions, prepago, modelo_credito)
    
    cosechas = credit.constructor.collection_of_vintages(producto, proyeccion, plazo, tasas, prepago,
                                      modelo_credito, presupuesto, 'consolidate')

    cosechas_total = cosechas.add(cosecha_contractual, fill_value = 0)
    credit.constructor.print_vintage(cosechas_total)
