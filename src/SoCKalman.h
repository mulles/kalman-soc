#pragma once

#include <stdint.h>

/**
 * @brief Calculated battery state of charge (SoC) using an extended kalman filter.
 *
 * Math currently uses floating point arithmetic. Can only record differences in SoC at a 30 min 
 * interval or greater.
 */
class SoCKalman
{
  public:
    SoCKalman();

    /**
     * @brief initial SoC is either passed in after being retrieved from local storage,
     * or is estimated based on starting battery voltage
     *
     * @param batteryEff, batteryVoltage, initialSoC (optional)
     */
    void init(bool isBattery12V,
              bool isBatteryLithium,
              uint32_t batteryEff,
              uint32_t batteryVoltage,
              uint32_t initialSoC);

    /**
     * @brief return current Soc in 0-100% bound. 
     *
     * @return uint32_t SoC
     */
    uint32_t read();

    /**
     * @brief return current battery efficiency
     *
     * @return uint32_t _batteryEff
     */
    uint32_t efficiency();


    /**
     * @brief calculate new SoC based on battery voltage as well as, how much power entered/exited
     * the battery in a given window  (TODO better use energy not power, imho power can't enter batteries
     * charge or energy does)
     * 
     * recalculate battery efficiency 
     *  
     * reset SoC = 100% if battery is in float
     *
     * @param isBatteryInFloat, isBatteryLithium, batteryMilliAmps, batteryVoltage,
     * batteryMilliWatts, samplePeriodMilliSec, batteryCapacityWattHour
     */
    void sample(bool isBatteryInFloat,
                int32_t batteryMilliAmps,
                uint32_t batteryVoltage, 
                int32_t batteryMilliWatts, 
                uint32_t samplePeriodMilliSec,
                uint32_t batteryCapacityWattHour);

  private:
    uint32_t _previousSoC;
    uint32_t _batteryEff;
    float _pval;
    float _qval;
    float _rval;
    float _pPre[9];
    float _pPost[9];
    float _q[9];
    float _a[9];
    float _at[9];
    float _h;
    float _H[3];
    float _Ht[3];
    float _G[3];
    bool _isBattery12V;
    bool _isBatteryLithium;
    uint32_t _millisecondsInFloat = 0;
    uint32_t _floatResetDuration = 600000;  // 10 minutes in milliseconds
    int32_t _x[3] = { 0, 0, 0 }; // state vector [SoC,R, hyteresis voltage?] /TODO
    uint8_t _n = 3;
    uint8_t _m = 1;
    const uint32_t SOC_SCALED_HUNDRED_PERCENT = 100000;  // 100% charge = 100000
    const uint32_t SOC_SCALED_MAX = 2 * SOC_SCALED_HUNDRED_PERCENT;  // allow SoC to track up higher
    // than 100% to gauge efficiency

    /**
     * @brief estimate an initial SoC based on battery voltage using a hardcoded OCV lookup table
     * for a given batteryVoltage it gives back a Soc, means inverse h function:  
     * x_k=h^-1(batteryVoltage)
     *
     * @param batteryVoltage
     *
     * @return uint32_t SoC
     */
    uint32_t calculateInitialSoC(uint32_t batteryVoltage);

    /**
     * @brief predict the state of charge ahead one step using a Coulomb counting model for the 
     * function f for the state space equation: 
     * f( x_k, p_k, \Delta t) = x_k - \frac{\Delta t}{Q} p_k 
     * with
     * SoC                                  x_k 
     * power in mW                          p_k
     * time period between measurements     \Delta t  
     * battery  capacity in Wh (constant)   Q     
     * 
     * calculates _batteryEff[0-1] based on the SoC at 10min in float charging mode. TODO If you do not
     * call the function with batteryEff > 0 it might always stay at 0 so would the SoC ? 
     * 
     * @param isBatteryinFloat, batteryMilliWatts, samplePeridoMilliSec, batteryCapacityWattHour
     * 
     * 
     * 
     */
    void f(bool isBatteryInFloat,
           int32_t batteryMilliWatts,
           uint32_t samplePeriodMilliSec,
           uint32_t batteryCapacityWattHour);

    /**
     * @brief predict measured battery voltage from the newly predicted state of charge _x using a 
     * h function for the measurement equation aka output equation: 
     * h(x_k) = OCV(x_k)
     * with
     * hardcoded OCV lookup table    OCV(x_k)
     * @param isBatteryLithium, batteryMilliAmps
     */
    void h(int32_t batteryMilliAmps);

    void diagonalMatrix(float value, float* result);

    void matMult(float* a, float* b, float* result, uint8_t arows, uint8_t acols, uint8_t bcols);

    void matMultConst(float* a, float b, float* result, uint8_t length);

    void matAdd(float* a, float* b, float* result, uint8_t length);

    void matAccum(float* a, float* b, uint8_t length);

    void transpose(float* a, float* result, uint8_t rows, uint8_t cols);

    void negate(float* a, uint8_t length);

    void updateState(float* a, uint8_t length);

    uint8_t inverse(float* a, float* result);

    uint32_t clamp(uint32_t value, uint32_t min, uint32_t max);

};
