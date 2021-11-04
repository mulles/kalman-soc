#pragma once

#include <stdint.h>

/**
 * @brief Calculated battery state of charge (SoC) using a extended kalman filter.
 * Math currently uses floating point arithmetic. Can only record diffreences in soc at a 30 min interval
 * or greater.
 */
class SoCKalman
{
  public:
    SoCKalman();

    /**
     * @brief initial soc is either passed in after being retrieved from local storage,
     *        or is estimated based on starting battery voltage
     *
     * @param batteryEff, batteryVoltage, initialSoC (optional)
     */
    void init(bool isBattery12V, bool isBatteryLithium, float batteryEff, float batteryVoltage, float initialSoC);

    /**
     * @brief return current state of charge
     *
     * @return float soc
     */
    float read();

    /**
     * @brief return current battery efficiency
     *
     * @return float _batteryEff
     */
    float efficiency();

    /**
     * @brief calculate new soc based on how much power entered/exited the battery in a given
     * window as well as the battery voltage, also recalculate battery efficiency and 
     * reset soc = 100% if battery is in float
     *
     * @param isBatteryInFloat, isBatteryLithium, batteryMilliAmps, batteryVoltage, batteryMilliWatts, samplePeriodMilliSec, batteryCapacity
     */
    void sample(bool isBatteryInFloat, float batteryMilliAmps, float batteryVoltage, float batteryMilliWatts, float samplePeriodMilliSec,
        float batteryCapacity);

  private:
    float _previousSoC;
    float _batteryEff;
    float _pval;      // P matrix init value (identity matrix)
    float _qval;      // Q matrix init value (identity matrix)
    float _rval;      // measurement error covariance scalar
    float _pPre[9];  // P, pre-update
    float _pPost[9]; // P, post-prediction
    float _q[9];     // process noise covariance 
    float _F[9];     // Jacobian of process model   
    float _Ft[9];    // transpose of process Jacobian
    float _h;      // output of user defined h() measurement function
    float _H[3];   // Jacobian of measurement model
    float _Ht[3];  // transpose of measurement Jacobian
    float _G[3];   // Kalman gain; aka K
    bool _isBattery12V;
    bool _isBatteryLithium;
    uint32_t _millisecondsInFloat = 0;
    uint32_t _floatResetDuration = 600000;  // 10 minutes in milliseconds
    float _x[3] = { 0, 0, 0 }; // state vector   with _x[0]=f() output of user defined state-transition function
    uint8_t _m = 1;  // number of state values 
    uint8_t _n = 3;  // number of observables 
    const uint32_t SOC_SCALED_HUNDRED_PERCENT = 100000;  // 100% charge = 100000
    const uint32_t SOC_SCALED_MAX = 2 * SOC_SCALED_HUNDRED_PERCENT;  // allow soc to track up higher than 100% to gauge efficiency

    /**
     * @brief estimate an initial soc based on battery voltage
     *
     * @param batteryVoltage
     *
     * @return float soc
     */
    float calculateInitialSoC(float batteryVoltage);

    /**
     * @brief project the state of charge ahead one step using a Coulomb counting model
     * 
     * @param isBatteryinFloat, batteryMilliWatts, samplePeridoMilliSec, batteryCapacity
     */
    void f(bool isBatteryInFloat, float batteryMilliAmps, float samplePeriodMilliSec, float batteryCapacity);

    /**
     * @brief predict the measurable value (voltage) ahead one step using the newly estimated state of charge
     * 
     * @param isBatteryLithium, batteryMilliAmps
     */
    void h(float batteryMilliAmps);

    void diagonalMatrix(float value, float* result);

    void matMult(float* a, float* b, float* result, uint8_t arows, uint8_t acols, uint8_t bcols);

    void matMultConst(float* a, float b, float* result, uint8_t length);

    void matAdd(float* a, float* b, float* result, uint8_t length);

    void matAccum(float* a, float* b, uint8_t length);

    void transpose(float* a, float* result, uint8_t rows, uint8_t cols);

    void negate(float* a, uint8_t length);

    void updateState(float* a, uint8_t length);

    uint8_t inverse(float* a, float* result);

    float clamp(float value, float min, float max);

};